"""
Agent CLI Commands

Command handlers for agent operations: create, list, edit, delete, start, stop, status.
"""

from pathlib import Path
from typing import Optional

from src.core.agent import AgentManager, AgentConfig, create_agent_from_form_data
from src.core.orchestrator import AgentOrchestrator
from src.security.encryption import Encryptor
from src.cli.theme import get_console, status_icon, platform_icon
from src.cli.menu import agent_form, select_agent, confirm
from src.utils.config import get_config
from src.utils.logger import get_logger


logger = get_logger(__name__)
console = get_console()

# Global orchestrators for running agents
_running_orchestrators: dict[str, AgentOrchestrator] = {}


def get_agent_manager() -> AgentManager:
    """Get agent manager instance"""
    # TODO: Get encryption manager from config/user input
    return AgentManager(encryption_manager=None)


def create_agent_command():
    """Create new agent"""
    console.rule("📝 Create New Agent", style="primary")
    console.print()
    
    # Show agent creation form
    form_data = agent_form()
    
    if not form_data:
        console.print_warning("Agent creation cancelled")
        return
    
    # Create agent
    try:
        manager = get_agent_manager()
        agent = create_agent_from_form_data(form_data)
        manager.save_agent(agent)
        
        console.print()
        console.print_success(f"Agent '{agent.name}' created successfully!")
        console.print(f"Description: {agent.config.description}")
        console.print(f"Platforms: {', '.join(agent.config.platforms.keys())}")
        console.print(f"WhatsApp groups: {len(agent.config.whatsapp_groups)}")
        
    except Exception as e:
        console.print_error(f"Failed to create agent: {e}")
        logger.error(f"Agent creation failed: {e}", exc_info=True)


def list_agents_command():
    """List all agents"""
    console.rule("📋 Configured Agents", style="primary")
    console.print()
    
    try:
        manager = get_agent_manager()
        agents = manager.list_agents()
        
        if not agents:
            console.print_warning("No agents configured yet")
            console.print()
            console.print("Create your first agent with the 'Create New Agent' option")
            return
        
        # Create table
        table = console.table(title=f"Total: {len(agents)} agent(s)")
        table.add_column("Name", style="cyan")
        table.add_column("Status", justify="center")
        table.add_column("Platforms", justify="center")
        table.add_column("Posts", justify="right")
        table.add_column("Description")
        
        for agent in agents:
            # Status icon and text
            status = status_icon(agent.status)
            
            # Platform icons
            platforms = " ".join(
                str(platform_icon(p)) for p in agent.config.platforms.keys()
            )
            
            # Add row
            table.add_row(
                agent.name,
                str(status),
                platforms or "-",
                str(agent.total_posts),
                agent.config.description or "-",
            )
        
        console.print(table)
        
    except Exception as e:
        console.print_error(f"Failed to list agents: {e}")
        logger.error(f"Agent listing failed: {e}", exc_info=True)


def edit_agent_command():
    """Edit existing agent"""
    console.rule("✏️  Edit Agent", style="primary")
    console.print()
    
    try:
        manager = get_agent_manager()
        agents = manager.list_agents()
        
        if not agents:
            console.print_warning("No agents to edit")
            return
        
        # Select agent
        agent_name = select_agent([a.to_dict() for a in agents])
        
        if not agent_name:
            console.print_warning("Edit cancelled")
            return
        
        agent = manager.get_agent(agent_name)
        
        if not agent:
            console.print_error(f"Agent not found: {agent_name}")
            return
        
        # Show edit form with existing data
        agent_data = agent.to_dict(include_credentials=False)
        form_data = agent_form(agent_data=agent_data["config"], edit_mode=True)
        
        if not form_data:
            console.print_warning("Edit cancelled")
            return
        
        # Update agent configuration
        agent.config.description = form_data.get("description", "")
        agent.config.whatsapp_phone = form_data["whatsapp"]["phone"]
        agent.config.whatsapp_groups = form_data["whatsapp"]["groups"]
        agent.config.auto_caption = form_data.get("auto_caption", True)
        agent.config.default_caption = form_data.get("default_caption", "")
        agent.config.hashtags = form_data.get("hashtags", [])
        agent.config.check_interval_minutes = form_data.get("check_interval_minutes", 5)
        
        # Update credentials if provided
        for platform, creds in form_data["platforms"].items():
            if "password" in creds:
                agent.set_credentials(
                    platform,
                    creds["username"],
                    creds["password"],
                )
        
        # Save changes
        manager.save_agent(agent)
        
        console.print()
        console.print_success(f"Agent '{agent.name}' updated successfully!")
        
    except Exception as e:
        console.print_error(f"Failed to edit agent: {e}")
        logger.error(f"Agent edit failed: {e}", exc_info=True)


def delete_agent_command():
    """Delete agent"""
    console.rule("🗑️  Delete Agent", style="primary")
    console.print()
    
    try:
        manager = get_agent_manager()
        agents = manager.list_agents()
        
        if not agents:
            console.print_warning("No agents to delete")
            return
        
        # Select agent
        agent_name = select_agent([a.to_dict() for a in agents])
        
        if not agent_name:
            console.print_warning("Delete cancelled")
            return
        
        # Confirm deletion
        if not confirm(f"Are you sure you want to delete agent '{agent_name}'?", default=False):
            console.print_warning("Delete cancelled")
            return
        
        # Stop orchestrator if running
        if agent_name in _running_orchestrators:
            console.print_info("Stopping running agent...")
            _running_orchestrators[agent_name].stop()
            del _running_orchestrators[agent_name]
        
        # Delete agent
        if manager.delete_agent(agent_name):
            console.print_success(f"Agent '{agent_name}' deleted successfully!")
        else:
            console.print_error(f"Failed to delete agent '{agent_name}'")
        
    except Exception as e:
        console.print_error(f"Failed to delete agent: {e}")
        logger.error(f"Agent deletion failed: {e}", exc_info=True)


def start_agent_command():
    """Start agent"""
    console.rule("▶️  Start Agent", style="primary")
    console.print()
    
    try:
        manager = get_agent_manager()
        agents = [a for a in manager.list_agents() if a.is_stopped]
        
        if not agents:
            console.print_warning("No stopped agents to start")
            return
        
        # Select agent
        agent_name = select_agent([a.to_dict() for a in agents])
        
        if not agent_name:
            console.print_warning("Start cancelled")
            return
        
        agent = manager.get_agent(agent_name)
        
        if not agent:
            console.print_error(f"Agent not found: {agent_name}")
            return
        
        # Check if already running
        if agent_name in _running_orchestrators:
            console.print_warning(f"Agent '{agent_name}' is already running")
            return
        
        # Start orchestrator
        console.print_info(f"Starting agent '{agent_name}'...")
        
        orchestrator = AgentOrchestrator(agent)
        
        if orchestrator.start():
            _running_orchestrators[agent_name] = orchestrator
            manager.save_agent(agent)
            
            console.print()
            console.print_success(f"Agent '{agent_name}' started successfully!")
            console.print(f"Monitoring {len(agent.config.whatsapp_groups)} WhatsApp group(s)")
            console.print(f"Posting to {len(agent.config.platforms)} platform(s)")
        else:
            console.print_error(f"Failed to start agent '{agent_name}'")
        
    except Exception as e:
        console.print_error(f"Failed to start agent: {e}")
        logger.error(f"Agent start failed: {e}", exc_info=True)


def stop_agent_command():
    """Stop agent"""
    console.rule("⏹️  Stop Agent", style="primary")
    console.print()
    
    try:
        manager = get_agent_manager()
        agents = [a for a in manager.list_agents() if a.is_running]
        
        if not agents:
            console.print_warning("No running agents to stop")
            return
        
        # Select agent
        agent_name = select_agent([a.to_dict() for a in agents])
        
        if not agent_name:
            console.print_warning("Stop cancelled")
            return
        
        # Stop orchestrator
        if agent_name not in _running_orchestrators:
            console.print_warning(f"Agent '{agent_name}' is not running")
            return
        
        console.print_info(f"Stopping agent '{agent_name}'...")
        
        orchestrator = _running_orchestrators[agent_name]
        orchestrator.stop()
        
        agent = manager.get_agent(agent_name)
        if agent:
            manager.save_agent(agent)
        
        del _running_orchestrators[agent_name]
        
        console.print()
        console.print_success(f"Agent '{agent_name}' stopped successfully!")
        
    except Exception as e:
        console.print_error(f"Failed to stop agent: {e}")
        logger.error(f"Agent stop failed: {e}", exc_info=True)


def status_command():
    """Show agent status and statistics"""
    console.rule("📊 Agent Status", style="primary")
    console.print()
    
    try:
        manager = get_agent_manager()
        agents = manager.list_agents()
        
        if not agents:
            console.print_warning("No agents configured")
            return
        
        # Overall statistics
        total_agents = len(agents)
        running_agents = len([a for a in agents if a.is_running])
        total_posts = sum(a.total_posts for a in agents)
        
        console.print(f"Total agents: {total_agents}")
        console.print(f"Running: {running_agents}")
        console.print(f"Total posts: {total_posts}")
        console.print()
        
        # Detailed status for each agent
        for agent in agents:
            panel_content = []
            
            # Status
            status = status_icon(agent.status)
            panel_content.append(f"Status: {status} {agent.status.upper()}")
            
            # Platforms
            platforms = " ".join(
                str(platform_icon(p)) for p in agent.config.platforms.keys()
            )
            panel_content.append(f"Platforms: {platforms}")
            
            # Statistics
            panel_content.append(f"Total posts: {agent.total_posts}")
            
            if agent.last_post:
                panel_content.append(f"Last post: {agent.last_post.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Orchestrator stats if running
            if agent.name in _running_orchestrators:
                orch = _running_orchestrators[agent.name]
                stats = orch.get_stats()
                panel_content.append(f"Videos processed: {stats['total_videos_processed']}")
                panel_content.append(f"Posts successful: {stats['total_posts_successful']}")
                panel_content.append(f"Posts failed: {stats['total_posts_failed']}")
            
            # Recent errors
            if agent.errors:
                panel_content.append(f"\n⚠️  Recent errors ({len(agent.errors)}):")
                for error in agent.errors[-3:]:  # Last 3 errors
                    panel_content.append(f"  • {error}")
            
            # Create panel
            panel = console.panel(
                "\n".join(panel_content),
                title=f"🤖 {agent.name}",
                subtitle=agent.config.description or None,
            )
            console.print(panel)
            console.print()
        
    except Exception as e:
        console.print_error(f"Failed to get status: {e}")
        logger.error(f"Status command failed: {e}", exc_info=True)


# Export commands
__all__ = [
    "create_agent_command",
    "list_agents_command",
    "edit_agent_command",
    "delete_agent_command",
    "start_agent_command",
    "stop_agent_command",
    "status_command",
]

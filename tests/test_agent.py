"""
Tests for agent management
"""

import pytest
import json
from pathlib import Path

from src.core.agent import Agent, AgentManager, AgentConfig, AgentStatus


class TestAgentConfig:
    """Test AgentConfig dataclass"""
    
    def test_agent_config_creation(self):
        """Test AgentConfig creation"""
        config = AgentConfig(
            name="test-agent",
            description="Test description",
        )
        assert config.name == "test-agent"
        assert config.description == "Test description"
    
    def test_agent_config_to_dict(self):
        """Test AgentConfig to_dict"""
        config = AgentConfig(name="test-agent")
        data = config.to_dict()
        assert isinstance(data, dict)
        assert data["name"] == "test-agent"
    
    def test_agent_config_from_dict(self):
        """Test AgentConfig from_dict"""
        data = {"name": "test-agent", "description": "Test"}
        config = AgentConfig.from_dict(data)
        assert config.name == "test-agent"
        assert config.description == "Test"


class TestAgent:
    """Test Agent class"""
    
    def test_agent_initialization(self):
        """Test Agent initialization"""
        config = AgentConfig(name="test-agent")
        agent = Agent(config)
        assert agent.name == "test-agent"
        assert agent.status == AgentStatus.STOPPED
    
    def test_agent_status_changes(self):
        """Test agent status changes"""
        config = AgentConfig(name="test-agent")
        agent = Agent(config)
        
        assert agent.is_stopped
        assert not agent.is_running
        
        agent.status = AgentStatus.RUNNING
        assert agent.is_running
        assert not agent.is_stopped
    
    def test_agent_to_dict(self):
        """Test agent serialization"""
        config = AgentConfig(name="test-agent")
        agent = Agent(config)
        
        data = agent.to_dict()
        assert isinstance(data, dict)
        assert data["config"]["name"] == "test-agent"
    
    def test_agent_from_dict(self):
        """Test agent deserialization"""
        config = AgentConfig(name="test-agent")
        agent = Agent(config)
        
        # Serialize and deserialize
        data = agent.to_dict(include_credentials=True)
        restored = Agent.from_dict(data)
        
        assert restored.name == agent.name
        assert restored.status == agent.status


class TestAgentManager:
    """Test AgentManager"""
    
    def test_agent_manager_initialization(self, mock_env):
        """Test AgentManager initialization"""
        manager = AgentManager(storage_dir=mock_env / "agents")
        assert manager.storage_dir.exists()
    
    def test_create_agent(self, mock_env):
        """Test agent creation"""
        manager = AgentManager(storage_dir=mock_env / "agents")
        config = AgentConfig(name="test-agent")
        
        agent = manager.create_agent(config)
        assert agent.name == "test-agent"
        assert manager.agent_exists("test-agent")
    
    def test_load_agent(self, mock_env):
        """Test agent loading"""
        manager = AgentManager(storage_dir=mock_env / "agents")
        config = AgentConfig(name="test-agent")
        
        # Create and save
        agent = manager.create_agent(config)
        
        # Load in new manager instance
        manager2 = AgentManager(storage_dir=mock_env / "agents")
        loaded = manager2.load_agent("test-agent")
        
        assert loaded is not None
        assert loaded.name == "test-agent"
    
    def test_delete_agent(self, mock_env):
        """Test agent deletion"""
        manager = AgentManager(storage_dir=mock_env / "agents")
        config = AgentConfig(name="test-agent")
        
        agent = manager.create_agent(config)
        assert manager.agent_exists("test-agent")
        
        manager.delete_agent("test-agent")
        assert not manager.agent_exists("test-agent")
    
    def test_list_agents(self, mock_env):
        """Test listing all agents"""
        manager = AgentManager(storage_dir=mock_env / "agents")
        
        # Create multiple agents
        for i in range(3):
            config = AgentConfig(name=f"agent-{i}")
            manager.create_agent(config)
        
        agents = manager.list_agents()
        assert len(agents) == 3
    
    def test_get_agent(self, mock_env):
        """Test getting agent by name"""
        manager = AgentManager(storage_dir=mock_env / "agents")
        config = AgentConfig(name="test-agent")
        manager.create_agent(config)
        
        agent = manager.get_agent("test-agent")
        assert agent is not None
        assert agent.name == "test-agent"
    
    def test_get_nonexistent_agent(self, mock_env):
        """Test getting nonexistent agent"""
        manager = AgentManager(storage_dir=mock_env / "agents")
        agent = manager.get_agent("nonexistent")
        assert agent is None


@pytest.mark.unit
class TestAgentSmokeTests:
    """Smoke tests for agent module"""
    
    def test_agent_module_importable(self):
        """Test agent module can be imported"""
        from src.core import agent
        assert hasattr(agent, 'Agent')
        assert hasattr(agent, 'AgentManager')
        assert hasattr(agent, 'AgentConfig')
        assert hasattr(agent, 'AgentStatus')

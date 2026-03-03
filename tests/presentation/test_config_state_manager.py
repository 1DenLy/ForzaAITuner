"""
Tests for ConfigStateManager — application-layer state container.

Covers:
  - update_config saves to repository and notifies subscribers
  - update_config raises ConfigLockedError when is_recording_session=True
  - is_recording_session flag correctly blocks/unblocks updates
  - subscribe() is idempotent (no duplicate notifications)
  - initialize() loads persisted config via model_factory
  - get_config() returns None before any config is set
"""

import pytest
from unittest.mock import MagicMock, call

from desktop_client.application.config_state_manager import ConfigStateManager
from desktop_client.application.exceptions import ConfigLockedError


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

class _FakeConfig:
    """Minimal stand-in for a Pydantic model."""
    def model_dump(self, **kwargs):
        return {"fake": "data"}


@pytest.fixture
def mock_repo():
    repo = MagicMock()
    repo.load_raw_data.return_value = {}   # empty by default
    return repo


@pytest.fixture
def manager(mock_repo):
    return ConfigStateManager(mock_repo)


# ---------------------------------------------------------------------------
# Basic state
# ---------------------------------------------------------------------------

class TestInitialState:
    def test_get_config_returns_none_before_any_update(self, manager):
        assert manager.get_config() is None

    def test_is_recording_session_defaults_to_false(self, manager):
        assert manager.is_recording_session is False


# ---------------------------------------------------------------------------
# update_config — happy path
# ---------------------------------------------------------------------------

class TestUpdateConfig:
    def test_update_config_sets_current_config(self, manager):
        cfg = _FakeConfig()
        manager.update_config(cfg)
        assert manager.get_config() is cfg

    def test_update_config_saves_to_repository(self, manager, mock_repo):
        cfg = _FakeConfig()
        manager.update_config(cfg)
        mock_repo.save_raw_data.assert_called_once_with({"fake": "data"})

    def test_update_config_notifies_subscribers(self, manager):
        subscriber = MagicMock()
        manager.subscribe(subscriber)

        cfg = _FakeConfig()
        manager.update_config(cfg)

        subscriber.assert_called_once_with(cfg)

    def test_update_config_notifies_all_subscribers(self, manager):
        sub_a, sub_b = MagicMock(), MagicMock()
        manager.subscribe(sub_a)
        manager.subscribe(sub_b)

        cfg = _FakeConfig()
        manager.update_config(cfg)

        sub_a.assert_called_once_with(cfg)
        sub_b.assert_called_once_with(cfg)


# ---------------------------------------------------------------------------
# Session lock — the critical race-condition guard
# ---------------------------------------------------------------------------

class TestSessionLock:
    def test_update_config_raises_when_session_active(self, manager):
        """The core race-condition guard must fire when the pipeline is running."""
        manager.is_recording_session = True

        with pytest.raises(ConfigLockedError):
            manager.update_config(_FakeConfig())

    def test_update_config_does_not_save_when_locked(self, manager, mock_repo):
        manager.is_recording_session = True

        with pytest.raises(ConfigLockedError):
            manager.update_config(_FakeConfig())

        mock_repo.save_raw_data.assert_not_called()

    def test_update_config_does_not_notify_when_locked(self, manager):
        subscriber = MagicMock()
        manager.subscribe(subscriber)
        manager.is_recording_session = True

        with pytest.raises(ConfigLockedError):
            manager.update_config(_FakeConfig())

        subscriber.assert_not_called()

    def test_update_config_succeeds_after_session_ends(self, manager):
        """Lock is released → next update must go through."""
        manager.is_recording_session = True
        manager.is_recording_session = False   # session ended

        cfg = _FakeConfig()
        manager.update_config(cfg)             # must not raise

        assert manager.get_config() is cfg

    def test_flag_can_be_toggled_externally(self, manager):
        """Composition root sets this flag via session_state_changed subscriber."""
        assert manager.is_recording_session is False
        manager.is_recording_session = True
        assert manager.is_recording_session is True
        manager.is_recording_session = False
        assert manager.is_recording_session is False


# ---------------------------------------------------------------------------
# subscribe() idempotency
# ---------------------------------------------------------------------------

class TestSubscribe:
    def test_duplicate_subscribe_does_not_double_notify(self, manager):
        subscriber = MagicMock()
        manager.subscribe(subscriber)
        manager.subscribe(subscriber)   # second call must be ignored

        manager.update_config(_FakeConfig())

        assert subscriber.call_count == 1


# ---------------------------------------------------------------------------
# initialize()
# ---------------------------------------------------------------------------

class TestInitialize:
    def test_initialize_loads_persisted_config(self, mock_repo):
        raw = {"persisted": True}
        mock_repo.load_raw_data.return_value = raw

        factory = MagicMock(return_value=_FakeConfig())
        mgr = ConfigStateManager(mock_repo)
        mgr.initialize(factory)

        factory.assert_called_once_with(raw)
        assert mgr.get_config() is not None

    def test_initialize_with_empty_repo_leaves_config_none(self, mock_repo):
        mock_repo.load_raw_data.return_value = {}
        mgr = ConfigStateManager(mock_repo)
        mgr.initialize(MagicMock())

        assert mgr.get_config() is None

    def test_initialize_with_invalid_data_leaves_config_none(self, mock_repo):
        mock_repo.load_raw_data.return_value = {"bad": "data"}
        factory = MagicMock(side_effect=ValueError("bad schema"))

        mgr = ConfigStateManager(mock_repo)
        mgr.initialize(factory)   # must not raise

        assert mgr.get_config() is None

import asyncio
import pytest
from desktop_client.infrastructure.sync.local_buffer import LocalBuffer


def test_put_and_size():
    buffer = LocalBuffer()
    buffer.put_nowait(1)
    buffer.put_nowait(2)
    buffer.put_nowait(3)
    assert buffer.size == 3


def test_ring_buffer_overflow():
    buffer = LocalBuffer(maxsize=3)
    buffer.put_nowait(1)
    buffer.put_nowait(2)
    buffer.put_nowait(3)
    buffer.put_nowait(4)
    # The oldest element (1) is pushed out
    assert buffer.size == 3
    with buffer.transaction_n(3) as batch:
        assert batch == [2, 3, 4]


def test_transaction_n_commit():
    """Successful block → items are removed from the buffer."""
    buffer = LocalBuffer()
    for i in range(1, 6):
        buffer.put_nowait(i)

    with buffer.transaction_n(3) as batch:
        assert len(batch) == 3
        assert batch == [1, 2, 3]

    assert buffer.size == 2


def test_transaction_n_locks_pending():
    """Second take_batch inside pending state returns the same batch."""
    buffer = LocalBuffer()
    buffer.put_nowait(1)
    buffer.put_nowait(2)
    buffer.put_nowait(3)

    # Take a batch without committing
    batch1 = buffer.take_batch(2)
    assert batch1 == [1, 2]

    # While pending, another take_batch returns the same items
    batch2 = buffer.take_batch(2)
    assert batch2 == [1, 2]  # Same batch returned

    # Clean up
    buffer._commit()


def test_transaction_n_rollback_on_exception():
    """Exception inside the block triggers automatic rollback, preserving order."""
    buffer = LocalBuffer()
    buffer.put_nowait(1)
    buffer.put_nowait(2)
    buffer.put_nowait(3)

    with pytest.raises(ValueError):
        with buffer.transaction_n(2) as batch:
            assert batch == [1, 2]
            raise ValueError("send failed")

    # After rollback the full queue is restored
    with buffer.transaction_n(3) as batch2:
        assert batch2 == [1, 2, 3]


def test_transaction_n_rollback_on_base_exception():
    """BaseException (e.g. CancelledError) also triggers rollback via finally."""
    buffer = LocalBuffer()
    buffer.put_nowait(1)
    buffer.put_nowait(2)

    with pytest.raises(asyncio.CancelledError):
        with buffer.transaction_n(2) as batch:
            assert batch == [1, 2]
            raise asyncio.CancelledError()

    # Items must be back in the queue after rollback
    assert buffer.size == 2
    with buffer.transaction_n(2) as batch2:
        assert batch2 == [1, 2]


def test_transaction_all_remaining():
    """transaction() grabs everything; commit clears the buffer."""
    buffer = LocalBuffer()
    buffer.put_nowait(1)
    buffer.put_nowait(2)
    buffer.put_nowait(3)

    # Grab one item into pending first
    batch1 = buffer.take_batch(1)
    assert batch1 == [1]

    with buffer.transaction() as all_remaining:
        assert all_remaining == [1, 2, 3]

    assert buffer.size == 0


def test_transaction_all_remaining_rollback():
    """Failed flush rolls back all remaining items."""
    buffer = LocalBuffer()
    for i in range(1, 4):
        buffer.put_nowait(i)

    with pytest.raises(RuntimeError):
        with buffer.transaction() as remaining:
            assert remaining == [1, 2, 3]
            raise RuntimeError("flush failed")

    assert buffer.size == 3


def test_take_all_remaining_pep8():
    """Verify PEP 8 snake_case method name is used (no UPPER)."""
    buffer = LocalBuffer()
    buffer.put_nowait(42)
    result = buffer.take_all_remaining()
    assert result == [42]
    buffer._commit()

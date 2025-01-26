from database import AsyncSessionLocal


async def get_db():
    """ Session generator """
    async_session = AsyncSessionLocal()
    try:
        yield async_session
    except Exception as e:
        await async_session.rollback()
    finally:
        await async_session.close()

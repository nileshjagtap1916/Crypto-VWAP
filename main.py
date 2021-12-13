from business.business import Business
import asyncio

if __name__ == '__main__':
    try:
        # create async await loop to avoid miscalculation
        loop = asyncio.get_event_loop()

        # Create business class object
        obj = Business(loop)

        # run receive_message task
        tasks = [
            asyncio.ensure_future(obj.receive_message())
        ]

        loop.run_until_complete(asyncio.wait(tasks))

        loop.close()
    except:
        print("Program closed.")

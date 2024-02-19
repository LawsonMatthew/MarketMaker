import asyncio
from frameworks.sharedstate import SharedState
#from strategy.basic import BasicAdding

async def main():
    ss = SharedState()
    #strategy = asyncio.create_task(BasicAdding(ss).run())
    ss_task = asyncio.create_task(ss.stream())
    await asyncio.gather(ss_task)

    #await Strategy(mdss, pdss, params).run()

if __name__ == "__main__":
    try:
        CONFIGURATION_DIR = ""  # Set your configuration directory path
        PARAMETERS_DIR = ""  # Set your parameter directory path

        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except asyncio.CancelledError:
        pass

#SOMETHING LIKE THIS

# import asyncio
# from frameworks.sharedstate import SharedState
# from stink_biddor.strategy.stinkbiddor import StinkBiddor
# from stink_biddor.settings import StinkBiddorParameters
# from frameworks.tools.logger import Logger, now


# async def main():
#     try:
#         parameters_directory = ""
#         params = StinkBiddorParameters(parameters_directory)

#         ss = SharedState()
#         ss.load_markets(params.pair)

#         await asyncio.gather(
#             asyncio.to_thread(params.refresh_parameters()),
#             asyncio.to_thread(StinkBiddor(ss, params).run())
#         )

#     except Exception as e:
#         Logger.critical(f"High level exception occurred, shutting down...")
#         # TODO: Implement shut down routine without sharedstate use
#         raise e

#     finally:
#         print(f"It's {now()}, goodnight...")
        
# if __name__ == "__main__":
#     asyncio.run(main())
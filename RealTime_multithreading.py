import threading
import RealTime_Data_collection as RTData_collection
import RealTime_2hour as RT2hour
import RealTime_10min as RT10min
import RealTime_ve as ve
import RealTime_nve as nve
import RealTime_rv as rv
import RealTime_nrv as nrv





def Data_collection():
	RTData_collection.begin()


def TwohourEvent():
	RT2hour.begin()

def TenminEvent():
	RT10min.begin()


def veEvent():
	ve.begin()

def nveEvent():
	nve.begin()

def rvEvent():
	rv.begin()

def nrvEvent():
	nrv.begin()


if __name__ == '__main__':
    RealTime_Data_collection_thread = threading.Thread(target=Data_collection)
    RealTime_2hour_thread = threading.Thread(target=TwohourEvent)
    RealTime_10min_thread = threading.Thread(target=TenminEvent)
    RealTime_ve_event = threading.Thread(target=veEvent)
    RealTime_nve_event = threading.Thread(target=nveEvent)
    RealTime_rv_event = threading.Thread(target=rvEvent)
    RealTime_nrv_event = threading.Thread(target=nrvEvent)



    RealTime_Data_collection_thread.start()
    RealTime_2hour_thread.start()
    RealTime_10min_thread.start()
    RealTime_ve_event.start()
    RealTime_nve_event.start()
    RealTime_rv_event.start()
    RealTime_nrv_event.start()
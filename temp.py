from multiprocessing import Process, Pipe
import time

def a(con_b):
    i=0
    while True:
        res_b=con_b.poll(timeout=1)
        if res_b:
            res=con_b.recv()
            print("result frob b ",res)
        print("i on a ",i)
        con_b.send(i)
        time.sleep(1)
        i+=1
def b(con_a):
    while True:
        res=con_a.recv()
        print("result from a ",res)
        time.sleep(5)
        con_a.send("ok")
    

if __name__=="__main__":
    con_a,con_b=Pipe()
    p1=Process(target=a,args=(con_b,))
    p2=Process(target=b,args=(con_a,))

    p1.start()
    p2.start()

    p2.join()
    p1.join()

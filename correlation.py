import numpy
def period(a):
    per = 0
    length_voice=len(a)
    R=[]
    temp=0
    for i in range (1,800): #i是自相关差
        temp=0
        for j in range(1,length_voice-i):
            temp=temp+a[j]*a[j+i]
        R.append(temp)
    print(R)
    r = numpy.array(R)
    per = numpy.argmax(r)+1
    return per

a=[1,2,3,-4,7,8,3,8,-9,1,2,4,-4,-6,
1,2,3,-4,7,9,3,8,-8,1,2,4,-4,-6,
1,2,3,-4,7,8,3,8,-9,1,2,4,-4,-6,
1,2,3,-4,7,9,3,8,-8,1,2,4,-4,-6,
1,2,3,-4,7,8,3,9,-9,1,2,4,-4,-6,
    1,2,3,-4,7,8,3,9,-9,1,2,4,-4,-6,
    1,2,3,-4,7,8,3,9,-9,1,2,4,-4,-6,
1,2,3,-4]

per = period(a)
frequence = 1/per
print(frequence)



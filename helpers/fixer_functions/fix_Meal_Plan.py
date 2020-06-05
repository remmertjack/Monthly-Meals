import random

def fx_month(month):
    if len(str(month))>1:
        mth = month
    else:
        mth = str(0) + str(month)
    return mth

def fx_cats(li):
    random.shuffle(li)
    while li[0]==li[1] or li[1]==li[2] or li[2]==li[3] or li[3]==li[4]:
        for i in range(0,len(li)):
            for j in range(1, len(li)):
                if li[i]==li[j]:
                    k = (i+1)%len(li)
                    li[j],li[k] = li[k],li[j]
    return li
def fx_month(month):
    if len(str(month))>1:
        mth = month
    else:
        mth = str(0) + str(month)
    return mth

def fx_cats(li):
    ct = 0
    while li[0]==li[1] or li[1]==li[2] or li[2]==li[3] or li[3]==li[4]:
        for i in range(0,len(li)):
            for j in range(1, len(li)):
                if li[i]==li[j]:
                    k = (i+2)%len(li)
                    li[j],li[k] = li[k],li[j]
                if li[0]!=li[1] and li[1]!=li[2] and li[2]!=li[3] and li[3]!=li[4]:
                    return li
        ct+=1
        if ct > 5:
            return li
    return li
                    
    
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 18:32:59 2018

@author: andy
"""

def subsetGenerator(numList, n):
    if n == 0 :
        return list();
    
    size = len(numList);
    l = list();
    j = 0;
    while j < size:
        subNumList = list(numList);
        takeoutNUm = subNumList[j];
        subNumList.pop(j);
        subList = subsetGenerator(subNumList, n - 1);
        sizeSublist = len(subList);
        if sizeSublist == 0:
            subList.append(list([takeoutNUm]));
        else:
            for h in range(sizeSublist):
                if subList[h][0] > takeoutNUm:
                    subList[h].insert(0, takeoutNUm);
        sizeSublist = len(subList);
        for h in range(sizeSublist):
            if len(subList[h]) == n:
                l.append(subList[h]);
        j = j + 1;
        
    return l;
    
from mylib import Any, mrange, Generator

BACKWARDS:str = "BACKWARDS"
FORWARDS:str = "FORWARDS"
LEFT:str = "LEFT"
RIGHT:str = "RIGHT"

class Grail:
    extBuffer:list = None
    extBufferLen:int = None
    blockOrigin:str = None
    blockLen:int = None

def ArrayCopy(array1:list, pos1:int, array2:list, pos2:int, length:int) -> None:
    if length < 1: return
    array2[pos2:length + pos2] = array1[pos1:length + pos1]

def BinarySearchExclusive(array:list, start:int, length:int, target:Any) -> int:
    left:int = 0
    right:int = length

    while left < right:
        middle:int = (left + right) // 2
        comp = Compare(array[start + middle], target)
        if not comp: return -1
        if comp < 0: left = middle + 1
        else: right = middle

    return left

def BinarySearchLeft(array:list, start:int, length:int, target:Any) -> int:
    left:int = 0
    right:int = length

    while left < right:
        middle:int = (left + right) // 2
        if Compare(array[start + middle], target) < 0: left = middle + 1
        else: right = middle

    return left

def BinarySearchRight(array:list, start:int, length:int, target:Any) -> int:
    left:int = 0
    right:int = length

    while left < right:
        middle:int = (left + right) // 2
        if Compare(array[start + middle], target) > 0: right = middle
        else: left = middle + 1

    return right

def BuildBlocks(array:list, start:int, length:int, bufferLen:int) -> None:
    if Grail.extBuffer:
        if bufferLen < Grail.extBufferLen: extLen:int = bufferLen
        else:
            extLen:int = 1
            while extLen * 2 <= Grail.extBufferLen: extLen *= 2
        BuildOutOfPlace(array, start, length, bufferLen, extLen)
    else:
        SortPairsWithKeys(array, start, length)
        BuildInPlace(array, start - 2, length, 2, bufferLen)

def BuildInPlace(array:list, start:int, length:int, currentLen:int, bufferLen:int) -> None:
    for mergeLen in mrange(currentLen, bufferLen, 2):
        bufferOffset:int = mergeLen
        fullMerge:int = 2 * mergeLen
        mergeEnd:int = start + length - fullMerge
        mergeIndex:int = start

        while mergeIndex <= mergeEnd:
            MergeForwards(array, mergeIndex, mergeLen, mergeLen, bufferOffset)
            mergeIndex += fullMerge

        leftOver:int = length + start - mergeIndex
        if leftOver > mergeLen:
            MergeForwards(array, mergeIndex, mergeLen, leftOver - mergeLen, bufferOffset)
        else: Rotate(array, mergeIndex - mergeLen, mergeLen, leftOver)
        
        start -= mergeLen

    fullMerge:int = 2 * bufferLen
    lastBlock:int = length % fullMerge
    lastOffset:int = start + length - lastBlock

    if lastBlock <= bufferLen: Rotate(array, lastOffset, lastBlock, bufferLen)
    else: MergeBackwards(array, lastOffset, bufferLen, lastBlock - bufferLen, bufferLen)
    for mergeIndex in range(lastOffset - fullMerge, start - 1, - fullMerge):
        MergeBackwards(array, mergeIndex, bufferLen, bufferLen, bufferLen)

def BuildOutOfPlace(array:list, start:int, length:int, bufferLen:int, extLen:int) -> None:
    ArrayCopy(array, start - extLen, Grail.extBuffer, 0, extLen)
    SortPairs(array, start, length)
    mergeLen:int = 2
    start -= 2

    for mergeLen in mrange(2, extLen, 2):
        bufferOffset:int = mergeLen
        fullMerge:int = 2 * mergeLen
        mergeEnd:int = start + length - fullMerge
        mergeIndex:int = start

        while mergeIndex <= mergeEnd:
            MergeForwardsOutOfPlace(array, mergeIndex, mergeLen, mergeLen, bufferOffset)
            mergeIndex += fullMerge

        leftOver:int = length + start - mergeIndex
        if leftOver > mergeLen:
            MergeForwardsOutOfPlace(array, mergeIndex, mergeLen, leftOver - mergeLen, bufferOffset)
        else: ArrayCopy(array, mergeIndex, array, mergeIndex - mergeLen, leftOver)
        
        start -= mergeLen

    if extLen == bufferLen:
        fullMerge:int = 2 * bufferLen
        lastBlock:int = length % fullMerge
        lastOffset:int = start + length - lastBlock
        
        if lastBlock <= bufferLen: ArrayCopy(array, lastOffset, array, lastOffset + bufferLen, lastBlock)
        else: MergeBackwardsOutOfPlace(array, lastOffset, bufferLen, lastBlock - bufferLen, bufferLen)

        for mergeIndex in range(lastOffset - fullMerge, start - 1, - fullMerge):
            MergeBackwardsOutOfPlace(array, mergeIndex, bufferLen, bufferLen, bufferLen)
    else:
        ArrayCopy(Grail.extBuffer, 0, array, start + length, extLen)
        BuildInPlace(array, start, length, mergeLen, bufferLen)

def CollectKeys(array:list, start:int, length:int, idealKeys:int) -> int:
    keysFound:int = 1
    firstKey:int = 0
    key:int = 1
    
    while key < length and keysFound < idealKeys:
        insertPos:int = BinarySearchExclusive(array, start + firstKey, keysFound, array[start + key])
        if insertPos > -1:
            Rotate(array, start + firstKey, keysFound, key - (firstKey + keysFound))
            firstKey = key - keysFound
            if keysFound != insertPos:
                InsertBackwards(array, start + firstKey + insertPos, keysFound - insertPos)
            keysFound += 1
        key += 1
    Rotate(array, start, firstKey, keysFound)
    return keysFound

def CombineBackwards(array:list, firstKey:int, start:int, length:int, subarrayLen:int, blockLen:int) -> None:
    mergeLen:int = 2 * subarrayLen
    fullMerges:int = length // mergeLen
    lastSubarrays:int = length - (mergeLen * fullMerges)

    if lastSubarrays <= subarrayLen:
        length -= lastSubarrays
        lastSubarrays = 0

    blockCount:int = lastSubarrays // blockLen
    leftBlocks:int = subarrayLen // blockLen
    medianKey:Any = array[firstKey + leftBlocks]

    if lastSubarrays:
        offset:int = start + (fullMerges * mergeLen)
        SortBlocks(array, firstKey, offset, blockCount, leftBlocks, blockLen, True)
        lastFragment:int = lastSubarrays - (blockCount * blockLen)
        MergeBlocksBackwards(array, firstKey, medianKey, offset, blockCount, blockLen, lastFragment)
        SortKeys(array, firstKey, medianKey, blockCount, offset)
   
    blockCount = mergeLen // blockLen
    for mergeIndex in reversed(range(fullMerges)):
        offset:int = start + (mergeIndex * mergeLen)
        SortBlocks(array, firstKey, offset, blockCount, leftBlocks, blockLen, True)
        MergeBlocksBackwards(array, firstKey, medianKey, offset, blockCount, blockLen, 0)
        SortKeys(array, firstKey, medianKey, blockCount, offset)

def CombineBackwardsOutOfPlace(array:list, firstKey:int, start:int, length:int, subarrayLen:int, blockLen:int) -> None:
    mergeLen:int = 2 * subarrayLen
    fullMerges:int = length // mergeLen
    lastSubarrays:int = length - (mergeLen * fullMerges)

    if lastSubarrays <= subarrayLen:
        length -= lastSubarrays
        lastSubarrays = 0
    
    blockCount:int = lastSubarrays // blockLen
    leftBlocks:int = subarrayLen // blockLen
    medianKey:Any = array[firstKey + leftBlocks]

    if lastSubarrays:
        offset:int = start + (fullMerges * mergeLen)
        if lastSubarrays - subarrayLen <= blockLen:
            MergeBackwards(array, offset, subarrayLen, lastSubarrays - subarrayLen, blockLen)
        else:
            SortBlocks(array, firstKey, offset, blockCount, leftBlocks, blockLen, True)
            lastFragment:int = lastSubarrays - (blockCount * blockLen)
            MergeBlocksBackwardsOutOfPlace(array, firstKey, medianKey, offset, blockCount, blockLen, lastFragment)
            InsertSort(array, firstKey, blockCount)
        
    blockCount = mergeLen // blockLen
    for mergeIndex in reversed(range(fullMerges)):
        offset:int = start + (mergeIndex * mergeLen)
        SortBlocks(array, firstKey, offset, blockCount, leftBlocks, blockLen, True)
        MergeBlocksBackwardsOutOfPlace(array, firstKey, medianKey, offset, blockCount, blockLen, 0)
        InsertSort(array, firstKey, blockCount)

def CombineBlocks(array:list, start:int, length:int, bufferLen:int, subarrayLen:int, blockLen:int, keyLen:int, idealBuffer:bool) -> str:
    direction:str = FORWARDS
    subarrayLen *= 2
    extBuffer:list = Grail.extBuffer

    if idealBuffer:
        if not extBuffer:
            while length - bufferLen > subarrayLen:
                if direction == FORWARDS:
                    CombineForwards(array, start, start + bufferLen, length - bufferLen, subarrayLen, blockLen)
                    direction = BACKWARDS
                else:
                    CombineBackwards(array, start, start + keyLen, length - bufferLen, subarrayLen, blockLen)
                    direction = FORWARDS
                subarrayLen *= 2
        else:
            while length - bufferLen > subarrayLen:
                if direction == FORWARDS:
                    CombineForwardsOutOfPlace(array, start, start + bufferLen, length - bufferLen, subarrayLen, blockLen)
                    direction = BACKWARDS
                else:
                    CombineBackwardsOutOfPlace(array, start, start + keyLen, length - bufferLen, subarrayLen, blockLen)
                    direction = FORWARDS
                subarrayLen *= 2
    else:
        keyBuffer:int = keyLen // 2
        ShellSort(array, start, keyBuffer)

        if not extBuffer:
            while keyBuffer >= (2 * subarrayLen) / keyBuffer:
                if direction == FORWARDS:
                    CombineForwards(array, start, start + keyLen, length - keyLen, subarrayLen, keyBuffer)
                    direction = BACKWARDS
                else:
                    CombineBackwards(array, start, start + keyBuffer, length - keyLen, subarrayLen, keyBuffer)
                    direction = FORWARDS
                subarrayLen *= 2
        else:
            while keyBuffer >= (2 * subarrayLen) / keyBuffer:
                if direction == FORWARDS:
                    CombineForwardsOutOfPlace(array, start, start + keyLen, length - keyLen, subarrayLen, keyBuffer)
                    direction = BACKWARDS
                else:
                    CombineBackwardsOutOfPlace(array, start, start + keyBuffer, length - keyLen, subarrayLen, keyBuffer)
                    direction = FORWARDS
                subarrayLen *= 2

        if direction == BACKWARDS:
            bufferOffset:int = start + keyBuffer
            SwapBlocksBackwards(array, bufferOffset, bufferOffset + keyBuffer, length - keyLen)
            direction = FORWARDS

        ShellSort(array, start, keyLen)
        while length - keyLen > subarrayLen:
            LazyCombine(array, start, start + keyLen, length - keyLen, subarrayLen, (2 * subarrayLen) // keyLen)
            subarrayLen *= 2
    return direction

def CombineForwards(array:list, firstKey:int, start:int, length:int, subarrayLen:int, blockLen:int) -> None:
    mergeLen:int = 2 * subarrayLen
    fullMerges:int = length // mergeLen
    blockCount:int = mergeLen // blockLen
    lastSubarrays:int = length - (mergeLen * fullMerges)
    fastForwardLen:int = 0
    
    if lastSubarrays <= subarrayLen:
        if fullMerges % 2: fastForwardLen = lastSubarrays
        length -= lastSubarrays
        lastSubarrays = 0

    leftBlocks:int = subarrayLen // blockLen
    medianKey:Any = array[firstKey + leftBlocks]

    for mergeIndex in range(fullMerges):
        offset:int = start + (mergeIndex * mergeLen)
        SortBlocks(array, firstKey, offset, blockCount, leftBlocks, blockLen, False)
        MergeBlocksForwards(array, firstKey, medianKey, offset, blockCount, blockLen, 0, 0)
        SortKeys(array, firstKey, medianKey, blockCount, offset + mergeLen - blockLen)
    
    offset:int = start + (fullMerges * mergeLen)

    if lastSubarrays:
        blockCount = lastSubarrays // blockLen
        SortBlocks(array, firstKey, offset, blockCount, leftBlocks, blockLen, False)
        
        lastFragment:int = lastSubarrays - (blockCount * blockLen)
        lastMergeBlocks:int = CountLastMergeBlocks(array, offset, blockCount, blockLen) if lastFragment else 0
        smartMerges:int = blockCount - lastMergeBlocks

        if not smartMerges:
            leftLen:int = lastMergeBlocks * blockLen
            MergeForwards(array, offset, leftLen, lastFragment, blockLen)
        else:
            MergeBlocksForwards(array, firstKey, medianKey, offset, smartMerges, 
                                blockLen, lastMergeBlocks, lastFragment)
        SortKeys(array, firstKey, medianKey, blockCount, offset + lastSubarrays - blockLen)

        if fullMerges and not fullMerges % 2:
            SwapBlocksBackwards(array, offset - blockLen, offset, lastSubarrays)
    else:
        if not fastForwardLen:
            if fullMerges % 2 and fullMerges != 1:
                SwapBlocksBackwards(array, offset - blockLen - mergeLen, offset - blockLen, mergeLen)
        else:
            SwapBlocksForwards(array, offset - blockLen, offset, fastForwardLen)

def CombineForwardsOutOfPlace(array:list, firstKey:int, start:int, length:int, subarrayLen:int, blockLen:int) -> None:
    mergeLen:int = 2 * subarrayLen
    fullMerges:int = length // mergeLen
    blockCount:int = mergeLen // blockLen
    lastSubarrays:int = length - (mergeLen * fullMerges)
    fastForwardLen:int = 0

    if lastSubarrays <= subarrayLen:
        if fullMerges % 2: fastForwardLen = lastSubarrays
        length -= lastSubarrays
        lastSubarrays = 0

    leftBlocks:int = subarrayLen // blockLen
    medianKey:Any = array[firstKey + leftBlocks]

    for mergeIndex in range(fullMerges):
        offset:int = start + (mergeIndex * mergeLen)
        SortBlocks(array, firstKey, offset, blockCount, leftBlocks, blockLen, False)
        MergeBlocksForwardsOutOfPlace(array, firstKey, medianKey, offset, blockCount, blockLen, 0, 0)
        InsertSort(array, firstKey, blockCount)

    offset:int = start + (fullMerges * mergeLen)

    if lastSubarrays:
        blockCount = lastSubarrays // blockLen
        SortBlocks(array, firstKey, offset, blockCount, leftBlocks, blockLen, False)
        
        lastFragment:int = lastSubarrays - (blockCount * blockLen)
        lastMergeBlocks:int = CountLastMergeBlocks(array, offset, blockCount, blockLen) if lastFragment else 0
        smartMerges:int = blockCount - lastMergeBlocks

        if not smartMerges:
            leftLen:int = lastMergeBlocks * blockLen
            MergeForwardsOutOfPlace(array, offset, leftLen, lastFragment, blockLen)
        else:
            MergeBlocksForwardsOutOfPlace(array, firstKey, medianKey, offset, smartMerges, 
                                          blockLen, lastMergeBlocks, lastFragment)
        InsertSort(array, firstKey, blockCount)

        if fullMerges and not fullMerges % 2:
            ArrayCopy(array, offset - blockLen, array, offset, lastSubarrays)
    else:
        if not fastForwardLen:
            if fullMerges % 2 and fullMerges != 1:
                ArrayCopy(array, offset - blockLen - mergeLen, array, offset - blockLen, mergeLen)
        else:
            ArrayCopy(array, offset, array, offset - blockLen, fastForwardLen)

def CommonSort(array:list, start:int, length:int, extBuffer:list=None, extBufferLen:int=None) -> None:
    if length < 16: return InsertSort(array, start, length)
    blockLen:int = 4
    while blockLen ** 2 < length: blockLen *= 2
    
    keyLen:int = ((length - 1) // blockLen) + 1
    idealKeys:int = keyLen + blockLen
    keysFound:int = CollectKeys(array, start, length, idealKeys)
    idealBuffer:bool = False

    if keysFound < idealKeys:
        if keysFound == 1: return
        if keysFound < 4: return LazyStableSort(array, start, length)
        keyLen = blockLen
        blockLen = 0
        while keyLen > keysFound: keyLen //= 2
    else: idealBuffer = True

    bufferLen:int = blockLen + keyLen
    subarrayLen:int = blockLen if idealBuffer else keyLen

    if extBuffer:
        print("Buffer is full of bugs, don't use it yet")
        Grail.extBuffer = extBuffer
        Grail.extBufferLen = extBufferLen
    
    BuildBlocks(array, start + bufferLen, length - bufferLen, subarrayLen)

    direction:str = CombineBlocks(array, start, length, bufferLen, subarrayLen, blockLen, keyLen, idealBuffer)

    if direction == FORWARDS:
        ShellSort(array, start + keyLen, blockLen)
        LazyMergeForwards(array, start, bufferLen, length - bufferLen)
    else:
        LazyMergeForwards(array, start, keyLen, length - bufferLen)
        ShellSort(array, start + length - blockLen, blockLen)
        LazyMergeBufferBackwards(array, start, length - blockLen, blockLen)
    
    Grail.extBuffer = None
    Grail.extBufferLen = None

def Compare(num1:Any, num2:Any) -> int:
    try:
        if num1 == num2: return 0
        if num1 > num2: return 1
    except TypeError: pass
    return -1

def CountLastMergeBlocks(array:list, offset:int, blockCount:int, blockLen:int) -> int:
    blocksToMerge:int = 0
    lastRightFrag:int = offset + (blockCount * blockLen)
    prevLeftBlock:int = lastRightFrag - blockLen

    while blocksToMerge < blockCount and Compare(array[lastRightFrag], array[prevLeftBlock]) < 0:
        blocksToMerge += 1
        prevLeftBlock -= blockLen
    return blocksToMerge

def GetSubarray(array:list, currentKey:int, medianKey:Any) -> str:
    return LEFT if Compare(array[currentKey], medianKey) < 0 else RIGHT

def GroupKeys(array:list, left:int, right:int, medianKey:Any) -> None:
    while left < right and Compare(array[left], medianKey) < 0: left += 1
    for i in range(left + 1, right):
        if Compare(array[i], medianKey) < 0:
            InsertBackwards(array, left, i - left)
            left += 1

def HolyGrail(array:list) -> list:
    CommonSort(array, 0, len(array), None, None)
    return array

def HolyShell(array:list) -> list:
    ShellSort(array, 0, len(array))
    return array

def InsertBackwards(array:list, start:int, length:int) -> None:
    item:Any = array[start + length]
    ArrayCopy(array, start, array, start + 1, length)
    array[start] = item

def InsertForwards(array:list, start:int, length:int) -> None:
    item:Any = array[start]
    ArrayCopy(array, start + 1, array, start, length)
    array[start + length] = item

def InsertSort(array:list, start:int, length:int) -> None:
    for item in range(1, length):
        temp:Any = array[start + item]
        index:int = start + item - 1

        if Compare(array[index], temp) < 1: continue
        if Compare(array[start], temp) > 0:
            InsertBackwards(array, start, item)
            continue

        while Compare(array[index - 1], temp) > 0: index -= 1
        InsertBackwards(array, index, start + item - index)

def LazyCombine(array:list, firstKey:int, start:int, length:int, subarrayLen:int, blockLen:int) -> None:
    mergeLen:int = 2 * subarrayLen
    fullMerges:int = length // mergeLen
    blockCount:int = mergeLen // blockLen
    lastSubarrays:int = length - (mergeLen * fullMerges)

    if lastSubarrays <= subarrayLen:
        length -= lastSubarrays
        lastSubarrays = 0

    leftBlocks:int = subarrayLen // blockLen
    medianKey:Any = array[firstKey + leftBlocks]
    
    for mergeIndex in range(fullMerges):
        offset:int = start + (mergeIndex * mergeLen)
        SortBlocks(array, firstKey, offset, blockCount, leftBlocks, blockLen, False)
        LazyMergeBlocks(array, firstKey, medianKey, offset, blockCount, blockLen, 0, 0)
        LazySortKeys(array, firstKey, blockCount, medianKey)

    offset:int = start + (fullMerges * mergeLen)

    if lastSubarrays:
        blockCount = lastSubarrays // blockLen
        SortBlocks(array, firstKey, offset, blockCount, leftBlocks, blockLen, False)
        
        lastFragment:int = lastSubarrays - (blockCount * blockLen)
        lastMergeBlocks:int = CountLastMergeBlocks(array, offset, blockCount, blockLen) if lastFragment else 0
        smartMerges:int = blockCount - lastMergeBlocks

        if not smartMerges:
            leftLen:int = lastMergeBlocks * blockLen
            LazyMergeBackwards(array, offset, leftLen, lastFragment)
        else:
            LazyMergeBlocks(array, firstKey, medianKey, offset, smartMerges, 
                            blockLen, lastMergeBlocks, lastFragment)
        LazySortKeys(array, firstKey, blockCount, medianKey)

def LazyMergeBackwards(array:list, start:int, leftLen:int, rightLen:int) -> None:
    end:int = start + leftLen + rightLen - 1

    while rightLen:
        mergeLen:int = BinarySearchRight(array, start, leftLen, array[end])
        if mergeLen != leftLen:
            Rotate(array, start + mergeLen, leftLen - mergeLen, rightLen)
            end -= leftLen - mergeLen
            leftLen = mergeLen
        
        if not leftLen: break
        
        middle:int = start + leftLen
        while True:
            rightLen -= 1
            end -= 1
            if not rightLen or Compare(array[middle - 1], array[end]) > 0: break

def LazyMergeBlocks(array:list, firstKey:int, medianKey:Any, start:int, blockCount:int, blockLen:int, lastMergeBlocks:int, lastLen:int) -> None:
    nextBlock:int = start + blockLen
    Grail.blockLen = blockLen
    Grail.blockOrigin = GetSubarray(array, firstKey, medianKey)
    
    for index in range(1, blockCount):
        currBlock:int = nextBlock - Grail.blockLen
        nextBlockOrigin:str = GetSubarray(array, firstKey + index, medianKey)

        if nextBlockOrigin != Grail.blockOrigin:
            LocalLazyMerge(array, currBlock, Grail.blockLen, Grail.blockOrigin, blockLen)
        else: Grail.blockLen = blockLen
        nextBlock += blockLen
        
    currBlock:int = nextBlock - Grail.blockLen
    if lastLen:
        if Grail.blockOrigin == RIGHT:
            currBlock = nextBlock
            Grail.blockLen = blockLen * lastMergeBlocks
            Grail.blockOrigin = LEFT
        else: Grail.blockLen += blockLen * lastMergeBlocks
        LazyMergeBackwards(array, currBlock, Grail.blockLen, lastLen)

def LazyMergeBufferBackwards(array:list, start:int, leftLen:int, rightLen:int) -> None:
    end:int = start + leftLen + rightLen - 1

    while rightLen:
        mergeLen = BinarySearchLeft(array, start, leftLen, array[end])
        if mergeLen != leftLen:
            Rotate(array, start + mergeLen, leftLen - mergeLen, rightLen)
            end -= leftLen - mergeLen
            leftLen = mergeLen

        if not leftLen: break

        middle:int = start + leftLen
        while True:
            rightLen -= 1
            end -= 1
            if not rightLen or Compare(array[middle - 1], array[end]) > 0: break

def LazyMergeForwards(array:list, start:int, leftLen:int, rightLen:int) -> None:
    middle:int = start + leftLen
    
    while leftLen:
        mergeLen:int = BinarySearchLeft(array, middle, rightLen, array[start])
        if mergeLen:
            Rotate(array, start, leftLen, mergeLen)
            start += mergeLen
            middle += mergeLen
            rightLen -= mergeLen
        
        if not rightLen: break

        while True:
            start += 1
            leftLen -= 1
            if not leftLen or Compare(array[start], array[middle]) > 0: break  

def LazySortKeys(array:list, firstKey:int, keyCount:int, medianKey:Any) -> None:
    runLen:int = 8
    keysEnd:int = firstKey + keyCount
    i:int = firstKey

    while i + runLen < keysEnd:
        GroupKeys(array, i, i + runLen, medianKey)
        i += runLen
    GroupKeys(array, i, keysEnd, medianKey)

    while runLen < keyCount:
        fullMerge:int = 2 * runLen
        mergeEnd:int = keysEnd - fullMerge
        mergeIndex:int = firstKey

        while mergeIndex <= mergeEnd:
            MergeGroups(array, mergeIndex, mergeIndex + runLen, mergeIndex + fullMerge, medianKey)
            mergeIndex += fullMerge

        leftOver:int = keysEnd - mergeIndex
        if leftOver > runLen:
            MergeGroups(array, mergeIndex, mergeIndex + runLen, keysEnd, medianKey)
        runLen *= 2

def LazyStableSort(array:list, start:int, length:int) -> None:
    i:int = 0
    while i <= length - 16:
        InsertSort(array, i, 16)
        i += 16
    InsertSort(array, i, length - i)
    
    for mergeLen in mrange(16, length, 2):
        fullMerge:int = 2 * mergeLen
        mergeEnd:int = length - fullMerge
        mergeIndex:int = 0

        while mergeIndex <= mergeEnd:
            LazyMergeBackwards(array, start + mergeIndex, mergeLen, mergeLen)
            mergeIndex += fullMerge

        leftOver:int = length - mergeIndex
        if leftOver > mergeLen: LazyMergeBackwards(array, start + mergeIndex, mergeLen, leftOver - mergeLen)

def LocalLazyMerge(array:list, start:int, leftLen:int, leftOrigin:str, rightLen:int) -> None:
    middle:int = start + leftLen
    if leftOrigin == LEFT:
        if Compare(array[middle - 1], array[middle]) > 0:
            while leftLen:
                mergeLen:int = BinarySearchLeft(array, middle, rightLen, array[start])
                if mergeLen:
                    Rotate(array, start, leftLen, mergeLen)
                    start += mergeLen
                    middle += mergeLen
                    rightLen -= mergeLen
                
                if not rightLen:
                    Grail.blockLen = leftLen
                    return
                
                while True:
                    start += 1
                    leftLen -= 1 
                    if not leftLen or Compare(array[start], array[middle]) > 0: break
    else:
        if Compare(array[middle - 1], array[middle]) >= 0:
            while leftLen:
                mergeLen:int = BinarySearchRight(array, middle, rightLen, array[start])
                if mergeLen:
                    Rotate(array, start, leftLen, mergeLen)
                    start += mergeLen
                    middle += mergeLen
                    rightLen -= mergeLen
                
                if not rightLen:
                    Grail.blockLen = leftLen
                    return
                
                while True:
                    start += 1
                    leftLen -= 1
                    if not leftLen or Compare(array[start], array[middle]) >= 0: break

    Grail.blockLen = rightLen
    Grail.blockOrigin = RIGHT if leftOrigin == LEFT else LEFT

def LocalMergeBackwards(array:list, start:int, leftLen:int, rightLen:int, rightOrigin:str, bufferOffset:int) -> None:
    end:int = start - 1
    left:int = end + leftLen
    middle:int = left
    right:int = middle + rightLen
    buffer:int = right + bufferOffset

    if rightOrigin == RIGHT:
        while left > end and right > middle:
            if Compare(array[left], array[right]) > 0:
                Swap(array, buffer, left)
                left -= 1 
            else:
                Swap(array, buffer, right)
                right -= 1 
            buffer -= 1
    else:
        while left > end and right > middle:
            if Compare(array[left], array[right]) >= 0:
                Swap(array, buffer, left)
                left -= 1 
            else:
                Swap(array, buffer, right)
                right -= 1 
            buffer -= 1 

    if right > middle:
        rightFrag:int = right - middle
        SwapBlocksForwards(array, end + 1, middle + 1, rightFrag)
        Grail.blockLen = rightFrag
    else:
        Grail.blockLen = left - end
        Grail.blockOrigin = LEFT if rightOrigin == RIGHT else RIGHT

def LocalMergeBackwardsOutOfPlace(array:list, start:int, leftLen:int, rightLen:int, rightOrigin:str, bufferOffset:int) -> None:
    end:int = start - 1
    left:int = end + leftLen
    middle:int = left
    right:int = middle + rightLen
    buffer:int = right + bufferOffset

    if rightOrigin == RIGHT:
        while left > end and right > middle:
            if Compare(array[left], array[right]) > 0:
                array[buffer] = array[left]
                left -= 1 
            else:
                array[buffer] = array[right]
                right -= 1 
            buffer -= 1 
    else:
        while left > end and right > middle:
            if Compare(array[left], array[right]) >= 0:
                array[buffer] = array[left]
                left -= 1 
            else:
                array[buffer] = array[right]
                right -= 1 
            buffer -= 1 

    if right > middle:
        rightFrag:int = right - middle
        ArrayCopy(array, middle + 1, array, end + 1, rightFrag)
        Grail.blockLen = rightFrag
    else:
        Grail.blockLen = left - end
        Grail.blockOrigin = LEFT if rightOrigin == RIGHT else RIGHT

def LocalMergeForwards(array:list, start:int, leftLen:int, leftOrigin:str, rightLen:int, bufferOffset:int) -> None:
    buffer:int = start - bufferOffset
    left:int = start
    middle:int = start + leftLen
    right:int = middle
    end:int = middle + rightLen

    if leftOrigin == LEFT:
        while left < middle and right < end:
            if Compare(array[left], array[right]) < 1:
                Swap(array, buffer, left)
                left += 1
            else:
                Swap(array, buffer, right)
                right += 1
            buffer += 1
    else:
        while left < middle and right < end:
            if Compare(array[left], array[right]) < 0:
                Swap(array, buffer, left)
                left += 1
            else:
                Swap(array, buffer, right)
                right += 1
            buffer += 1

    if left < middle:
        leftFrag:int = middle - left
        SwapBlocksBackwards(array, left, end - leftFrag, leftFrag)
        Grail.blockLen = leftFrag
    else:
        Grail.blockLen = end - right
        Grail.blockOrigin = RIGHT if leftOrigin == LEFT else LEFT

def LocalMergeForwardsOutOfPlace(array:list, start:int, leftLen:int, leftOrigin:str, rightLen:int, bufferOffset:int) -> None:
    buffer:int = start - bufferOffset
    left:int = start
    middle:int = start + leftLen
    right:int = middle
    end:int = middle + rightLen

    if leftOrigin == LEFT:
        while left < middle and right < end:
            if Compare(array[left], array[right]) < 1:
                array[buffer] = array[left]
                left += 1
            else:
                array[buffer] = array[right]
                right += 1
            buffer += 1
    else:
        while left < middle and right < end:
            if Compare(array[left], array[right]) < 0:
                array[buffer] = array[left]
                left += 1
            else:
                array[buffer] = array[right]
                right += 1
            buffer += 1

    if left < middle:
        leftFrag:int = middle - left
        ArrayCopy(array, left, array, end - leftFrag, leftFrag)
        Grail.blockLen = leftFrag
    else:
        Grail.blockLen = end - right
        Grail.blockOrigin = RIGHT if leftOrigin == LEFT else LEFT

def MergeBackwards(array:list, start:int, leftLen:int, rightLen:int, bufferOffset:int) -> None:
    end:int = start - 1
    left:int = end + leftLen
    middle:int = left
    right:int = middle + rightLen
    buffer:int = right + bufferOffset

    while left > end:
        if right == middle or Compare(array[left], array[right]) > 0:
            Swap(array,buffer,left)
            left -= 1 
        else:
            Swap(array,buffer,right)
            right -= 1
        buffer -= 1

    if right != buffer: SwapBlocksBackwards(array, right, buffer, right - middle)

def MergeBackwardsOutOfPlace(array:list, start:int, leftLen:int, rightLen:int, bufferOffset:int) -> None:
    end:int = start - 1
    left:int = end + leftLen
    middle:int = left
    right:int = middle + rightLen
    buffer:int = right + bufferOffset
    
    while left > end:
        if right == middle or Compare(array[left], array[right]) > 0:
            array[buffer] = array[left]
            left-=1
        else:
            array[buffer] = array[right]
            right -= 1 
        buffer -= 1

    if right != buffer: ArrayCopy(array, right, array, buffer, right - middle)

def MergeBlocksBackwards(array:list, firstKey:int, medianKey:Any, start:int, blockCount:int, blockLen:int, lastLen:int) -> None:
    nextBlock:int = start + (blockCount * blockLen) - 1
    buffer:int = nextBlock + lastLen + blockLen
    Grail.blockLen = lastLen
    Grail.blockOrigin = RIGHT

    for index in reversed(range(blockCount)):
        nextBlockOrigin:str = GetSubarray(array, firstKey + index, medianKey)
        if nextBlockOrigin != Grail.blockOrigin:
            LocalMergeBackwards(array, nextBlock - blockLen + 1, blockLen, 
                                Grail.blockLen, Grail.blockOrigin, blockLen)
        else:
            buffer = nextBlock + blockLen + 1
            SwapBlocksBackwards(array, nextBlock + 1, buffer, Grail.blockLen)
            Grail.blockLen = blockLen
        nextBlock -= blockLen

    SwapBlocksBackwards(array, start, start + blockLen, Grail.blockLen)

def MergeBlocksBackwardsOutOfPlace(array:list, firstKey:int, medianKey:Any, start:int, blockCount:int, blockLen:int, lastLen:int) -> None:
    nextBlock:int = start + (blockCount * blockLen) - 1
    buffer:int = nextBlock + lastLen + blockLen
    Grail.blockLen = lastLen
    Grail.blockOrigin = RIGHT
    
    for index in reversed(range(blockCount)):
        nextBlockOrigin = GetSubarray(array, firstKey + index, medianKey)
        if nextBlockOrigin != Grail.blockOrigin:
            LocalMergeBackwardsOutOfPlace(array, nextBlock - blockLen + 1, blockLen, 
                                          Grail.blockLen, Grail.blockOrigin, blockLen)
        else:
            buffer = nextBlock + blockLen + 1
            ArrayCopy(array, nextBlock + 1, array, buffer, Grail.blockLen)
            Grail.blockLen = blockLen
        nextBlock -= blockLen

    ArrayCopy(array, start, array, start + blockLen, Grail.blockLen)

def MergeBlocksForwards(array:list, firstKey:int, medianKey:Any, start:int, blockCount:int, blockLen:int, lastMergeBlocks:int, lastLen:int) -> None:
    nextBlock:int = start + blockLen
    Grail.blockLen = blockLen
    Grail.blockOrigin = GetSubarray(array, firstKey, medianKey)

    for index in range(1, blockCount):
        currBlock:int = nextBlock - Grail.blockLen
        nextBlockOrigin:str = GetSubarray(array, firstKey + index, medianKey)

        if nextBlockOrigin != Grail.blockOrigin:
            LocalMergeForwards(array, currBlock, Grail.blockLen, Grail.blockOrigin, blockLen, blockLen)
        else:
            buffer:int = currBlock - blockLen
            SwapBlocksForwards(array, buffer, currBlock, Grail.blockLen)
            Grail.blockLen = blockLen
        nextBlock += blockLen
        
    currBlock:int = nextBlock - Grail.blockLen
    buffer:int = currBlock - blockLen

    if lastLen:
        if Grail.blockOrigin == RIGHT:
            SwapBlocksForwards(array, buffer, currBlock, Grail.blockLen)
            currBlock = nextBlock
            Grail.blockLen = blockLen * lastMergeBlocks
            Grail.blockOrigin = LEFT
        else: Grail.blockLen += blockLen * lastMergeBlocks
        MergeForwards(array, currBlock, Grail.blockLen, lastLen, blockLen)
    else: SwapBlocksForwards(array, buffer, currBlock, Grail.blockLen)

def MergeBlocksForwardsOutOfPlace(array:list, firstKey:int, medianKey:Any, start:int, blockCount:int, blockLen:int, lastMergeBlocks:int, lastLen:int) -> None:
    nextBlock:int = start + blockLen
    Grail.blockLen = blockLen
    Grail.blockOrigin = GetSubarray(array, firstKey, medianKey)

    for index in range(1, blockCount):
        currBlock:int = nextBlock - Grail.blockLen
        nextBlockOrigin:str = GetSubarray(array, firstKey + index, medianKey)

        if nextBlockOrigin != Grail.blockOrigin:
            LocalMergeForwardsOutOfPlace(array, currBlock, Grail.blockLen, Grail.blockOrigin, blockLen, blockLen)
        else:
            buffer:int = currBlock - blockLen
            ArrayCopy(array, currBlock, array, buffer, Grail.blockLen)
            Grail.blockLen = blockLen
        nextBlock += blockLen
    
    currBlock:int = nextBlock - Grail.blockLen
    buffer:int = currBlock - blockLen

    if lastLen:
        if Grail.blockOrigin == RIGHT:
            ArrayCopy(array, currBlock, array, buffer, Grail.blockLen)
            currBlock = nextBlock
            Grail.blockLen = blockLen * lastMergeBlocks
            Grail.blockOrigin = LEFT
        else: Grail.blockLen += blockLen * lastMergeBlocks
        MergeForwardsOutOfPlace(array, currBlock, Grail.blockLen, lastLen, blockLen)
    else: ArrayCopy(array, currBlock, array, buffer, Grail.blockLen)

def MergeForwards(array:list, start:int, leftLen:int, rightLen:int, bufferOffset:int) -> None:
    buffer:int = start - bufferOffset
    left:int = start
    middle:int = start + leftLen
    right:int = middle
    end:int = middle + rightLen

    while right < end:
        if left == middle or Compare(array[left], array[right]) > 0:
            Swap(array, buffer, right)
            right += 1
        else:
            Swap(array, buffer, left)
            left += 1
        buffer += 1

    if buffer != left: SwapBlocksForwards(array, buffer, left, middle - left)

def MergeForwardsOutOfPlace(array:list, start:int, leftLen:int, rightLen:int, bufferOffset:int) -> None:
    buffer:int = start - bufferOffset
    left:int = start
    middle:int = start + leftLen
    right:int = middle
    end:int = middle + rightLen

    while right < end:
        if left == middle or Compare(array[left], array[right]) > 0:
            Swap(array, buffer, right)
            right += 1
        else:
            Swap(array, buffer, left)
            left += 1
        buffer += 1

    if buffer != left: ArrayCopy(array, left, array, buffer, middle - left)

def MergeGroups(array:list, left:int, middle:int, right:int, medianKey:Any) -> None:
    leftLen:int = middle - left
    rightLen:int = right - middle
    mergeStart:int = left + BinarySearchLeft(array, left, leftLen, medianKey)
    mergeLen:int = BinarySearchLeft(array, middle, rightLen, medianKey)
    Rotate(array, mergeStart, middle - mergeStart, mergeLen)

def Rotate(array:list, start:int, leftLen:int, rightLen:int) -> None:
    minLen:int = leftLen if leftLen <= rightLen else rightLen
    while minLen > 1:
        if leftLen <= rightLen:
            while True:
                SwapBlocksForwards(array, start, start + leftLen, leftLen)
                start += leftLen
                rightLen -= leftLen
                if leftLen > rightLen: break
            minLen = rightLen
        else:
            while True:
                SwapBlocksBackwards(array, start + leftLen - rightLen, start + leftLen, rightLen)
                leftLen -= rightLen
                if leftLen <= rightLen: break
            minLen = leftLen

    if minLen == 1:
        if leftLen == 1: InsertForwards(array, start, rightLen)
        else: InsertBackwards(array, start, leftLen)

def ShellGaps(stop:int) -> Generator[int, None, None]:
    yield 3
    for i in range(stop):
        gap:int = 4 ** (i + 1) + 3 * 2 ** i + 1
        if gap >= stop: break
        yield gap

def ShellPass(array:list, start:int, length:int, gap:int) -> None:
    for item in range(gap, length):
        index:int = start + item
        temp:Any = array[index]

        if Compare(array[index - gap], temp) < 1: continue
        
        while True:
            array[index] = array[index - gap]
            index -= gap
            if index - gap <= start or Compare(array[index - gap], temp) < 1: break
        
        array[index] = temp

def ShellSort(array:list, start:int, length:int) -> None:
    for gap in reversed(tuple(ShellGaps(length))): 
        ShellPass(array, start, length, gap)
    InsertSort(array, start, length)

def SortBlocks(array:list, firstKey:int, start:int, blockCount:int, leftBlocks:int, blockLen:int, sortByTail:bool) -> None: 
    if blockCount == leftBlocks: return 
    
    cmpIndex:int = blockLen - 1 if sortByTail else 0
    blockIndex:int = start
    index:int = firstKey
    rightBlock:int = start + (leftBlocks * blockLen)
    rightKey:int = firstKey + leftBlocks
    sorted:bool = True

    while True:
        if Compare(array[rightBlock + cmpIndex], array[blockIndex + cmpIndex]) < 0:
            SwapBlocksForwards(array, blockIndex, rightBlock, blockLen)
            Swap(array, index, rightKey)
            sorted = False
        blockIndex += blockLen
        index += 1
        if not sorted or index >= rightKey: break
    
    if sorted: return

    lastKey:int = firstKey + blockCount - 1
    scrambledEnd:int = rightKey + 1 if rightKey < lastKey else rightKey

    while index < rightKey:
        selectBlock:int = rightBlock
        selectKey:int = rightKey
        currBlock:int = rightBlock + blockLen
        
        for key in range(rightKey + 1, scrambledEnd + 1):
            compare = Compare(array[currBlock + cmpIndex], array[selectBlock + cmpIndex])
            if compare < 0 or not compare and Compare(array[key], array[selectKey]) < 0:
                selectBlock, selectKey = currBlock, key
            currBlock += blockLen

        SwapBlocksForwards(array, blockIndex, selectBlock, blockLen)
        Swap(array, index, selectKey)

        if selectKey == scrambledEnd and scrambledEnd < lastKey: scrambledEnd += 1
        blockIndex += blockLen
        index += 1

    while scrambledEnd < lastKey:
        selectBlock:int = blockIndex
        selectKey:int = index
        currBlock:int = blockIndex + blockLen

        for key in range(index + 1, scrambledEnd + 1):
            compare = Compare(array[currBlock + cmpIndex], array[selectBlock + cmpIndex])
            if compare < 0 or not compare and Compare(array[key], array[selectKey]) < 0:
                selectBlock, selectKey = currBlock, key
            currBlock += blockLen

        if selectKey != index:
            SwapBlocksForwards(array, blockIndex, selectBlock, blockLen)
            Swap(array, index, selectKey)
            if selectKey == scrambledEnd: scrambledEnd += 1

        blockIndex += blockLen
        index += 1

        if index == scrambledEnd: return
    
    while True:
        selectBlock:int = blockIndex
        selectKey:int = index
        currBlock:int = blockIndex + blockLen
        
        for key in range(index + 1, lastKey + 1):
            compare = Compare(array[currBlock + cmpIndex], array[selectBlock + cmpIndex])
            if compare < 0 or not compare and Compare(array[key], array[selectKey]) < 0:
                selectBlock, selectKey = currBlock, key
            currBlock += blockLen

        if selectKey != index:
            SwapBlocksForwards(array, blockIndex, selectBlock, blockLen)
            Swap(array, index, selectKey)
        
        blockIndex += blockLen
        index += 1

        if not index < lastKey: break

def SortKeys(array:list, firstKey:int, medianKey:Any, keyCount:int, buffer:int) -> None:
    key:int = firstKey
    keysEnd:int = firstKey + keyCount
    bufferSwaps:int = 0

    while key < keysEnd:
        if Compare(array[key], medianKey) < 0:
            if bufferSwaps: Swap(array, key, key - bufferSwaps)
        else:
            Swap(array, key, buffer + bufferSwaps)
            bufferSwaps += 1
        key += 1
    SwapBlocksBackwards(array, key - bufferSwaps, buffer, bufferSwaps)

def SortPairs(array:list, start:int, length:int) -> None:
    index:int = 1
    while index < length:
        left:int = start + index - 1
        right:int = start + index
        if Compare(array[left], array[right]) > 0:
            array[left - 2] = array[right]
            array[right - 2] = array[left]
        else:
            array[left - 2] = array[left]
            array[right - 2] = array[right]
        index += 2

    left:int = start + index - 1
    if left < start + length:
        array[left - 2] = array[left]  

def SortPairsWithKeys(array:list, start:int, length:int) -> None:
    firstKey:Any = array[start - 1]
    secondKey:Any = array[start - 2]
    SortPairs(array, start, length)
    array[start + length - 2] = firstKey
    array[start + length - 1] = secondKey

def Swap(array:list, ind1:int, ind2:int):
    array[ind1], array[ind2] = array[ind2], array[ind1]

def SwapBlocksBackwards(array:list, a:int, b:int, blockLen:int) -> None:
    for i in reversed(range(blockLen)): Swap(array, a + i, b + i)

def SwapBlocksForwards(array:list, a:int, b:int, blockLen:int) -> None:
    for i in range(blockLen): Swap(array, a + i, b + i)
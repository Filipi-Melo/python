from mylib import Any

LEFT:int = 0
RIGHT:int = 1
GRAIL_STATIC_BUFFER_LEN:int = 512

class Grail:
    extBuffer:list = None
    extBufferLen:int = 0
    blockLen:int = None
    blockOrigin:int = None

def ArrayCopy(fromArray:list, fromIndex:int, toArray:list, toIndex:int, length:int) -> None:
    toArray[toIndex:toIndex + length] = fromArray[fromIndex:fromIndex + length]

def Compare(num1:Any, num2:Any) -> int:
    try:
        if num1 == num2: return 0
        if num1 > num2: return 1
    except TypeError: pass
    return -1

def GrailBinarySearchLeft(array:list, start:int, length:int, target:Any) -> int:
    left:int  = 0
    right:int = length

    while left < right:
        middle:int = left + ((right - left) // 2)
        if Compare(array[start + middle], target) < 0: left = middle + 1
        else: right = middle
    return left

def GrailBinarySearchRight(array:list, start:int, length:int, target:Any) -> int:
    left:int  = 0
    right:int = length

    while left < right:
        middle:int = left + ((right - left) // 2)
        if Compare(array[start + middle], target) > 0: right = middle
        else: left = middle + 1
    return right

def GrailBlockSwap(array:list, a:int, b:int, blockLen:int) -> None:
    for i in range(blockLen): GrailSwap(array, a + i, b + i)

def GrailBuildBlocks(array:list, start:int, length:int, bufferLen:int) -> None:
    if Grail.extBuffer:
        if bufferLen < Grail.extBufferLen: extLen:int = bufferLen
        else:
            extLen:int = 1
            while extLen * 2 <= Grail.extBufferLen: extLen *= 2
        GrailBuildOutOfPlace(array, start, length, bufferLen, extLen)
    else:
        GrailPairwiseSwaps(array, start, length)
        GrailBuildInPlace(array, start - 2, length, 2, bufferLen)   

def GrailBuildInPlace(array:list, start:int, length:int, currentLen:int, bufferLen:int) -> None:
    mergeLen:int = currentLen
    while mergeLen < bufferLen:
        fullMerge:int = 2 * mergeLen
        mergeEnd:int = start + length - fullMerge
        bufferOffset:int = mergeLen
        mergeIndex:int = start

        while mergeIndex <= mergeEnd:
            GrailMergeForwards(array, mergeIndex, mergeLen, mergeLen, bufferOffset)
            mergeIndex += fullMerge

        leftOver:int = length + start - mergeIndex
        if leftOver > mergeLen:
            GrailMergeForwards(array, mergeIndex, mergeLen, leftOver - mergeLen, bufferOffset)
        else: GrailRotate(array, mergeIndex - mergeLen, mergeLen, leftOver)

        start -= mergeLen
        mergeLen *= 2

    fullMerge:int = 2 * bufferLen
    lastBlock:int = length % fullMerge
    lastOffset:int = start + length - lastBlock

    if lastBlock <= bufferLen: GrailRotate(array, lastOffset, lastBlock, bufferLen)
    else: GrailMergeBackwards(array, lastOffset, bufferLen, lastBlock - bufferLen, bufferLen)

    mergeIndex:int = lastOffset - fullMerge
    while mergeIndex >= start:
        GrailMergeBackwards(array, mergeIndex, bufferLen, bufferLen, bufferLen)
        mergeIndex -= fullMerge
   
def GrailBuildOutOfPlace(array:list, start:int, length:int, bufferLen:int, extLen:int) -> None:
    ArrayCopy(array, start - extLen, Grail.extBuffer, 0, extLen)
    GrailPairwiseWrites(array, start, length)
    mergeLen:int = 2
    start -= 2

    while mergeLen < extLen:
        fullMerge:int = 2 * mergeLen
        mergeEnd:int = start + length - fullMerge
        bufferOffset:int = mergeLen
        mergeIndex:int = start

        while mergeIndex <= mergeEnd:
            GrailMergeOutOfPlace(array, mergeIndex, mergeLen, mergeLen, bufferOffset)
            mergeIndex += fullMerge

        leftOver:int = length + start - mergeIndex
        if leftOver > mergeLen:
            GrailMergeOutOfPlace(array, mergeIndex, mergeLen, leftOver - mergeLen, bufferOffset)
        else: ArrayCopy(array, mergeIndex, array, mergeIndex - mergeLen, leftOver)

        start -= mergeLen
        mergeLen *= 2
    
    ArrayCopy(Grail.extBuffer, 0, array, start + length, extLen)
    GrailBuildInPlace(array, start, length, mergeLen, bufferLen)

def GrailBlockSelectSort(array:list, firstKey:int, start:int, medianKey:int, blockCount:int, blockLen:int) -> int:
    for firstBlock in range(blockCount):
        selectBlock:int = firstBlock

        for currBlock in range(firstBlock + 1, blockCount):
            compare:int = Compare(array[start + (currBlock * blockLen)], array[start + (selectBlock * blockLen)])

            if compare < 0 or not compare and Compare(array[firstKey + currBlock], array[firstKey + selectBlock]) < 0:
                selectBlock = currBlock

        if selectBlock != firstBlock:
            GrailBlockSwap(array, start + (firstBlock * blockLen), start + (selectBlock * blockLen), blockLen)
            GrailSwap(array, firstKey + firstBlock, firstKey + selectBlock)

            if medianKey == firstBlock: medianKey = selectBlock
            elif medianKey == selectBlock: medianKey = firstBlock

    return medianKey

def GrailCollectKeys(array:list, start:int, length:int, idealKeys:int) -> int:
    keysFound:int = 1
    firstKey:int = 0
    key:int = 1

    while key < length and keysFound < idealKeys:
        insertPos:int = GrailBinarySearchLeft(array, start + firstKey, keysFound, array[start + key])
        if insertPos == keysFound or Compare(array[start + key], array[start + firstKey + insertPos]):
            GrailRotate(array, start + firstKey, keysFound, key - (firstKey + keysFound))
            firstKey = key - keysFound
            GrailRotate(array, start + firstKey + insertPos, keysFound - insertPos, 1)
            keysFound += 1
        key += 1
    GrailRotate(array, start, firstKey, keysFound)
    return keysFound

def GrailCombineBlocks(array:list, firstKey:int, start:int, length:int, subarrayLen:int, blockLen:int, buffer:bool) -> None:
    fullMerge:int = 2 * subarrayLen
    mergeCount:int = length // fullMerge
    lastSubarrays:int = length - (fullMerge * mergeCount)

    if lastSubarrays <= subarrayLen:
        length -= lastSubarrays
        lastSubarrays = 0

    if buffer and blockLen <= Grail.extBufferLen:
        GrailCombineOutOfPlace(array, firstKey, start, length, subarrayLen, blockLen, mergeCount, lastSubarrays)
    else:
        GrailCombineInPlace(array, firstKey, start, length, subarrayLen, blockLen, mergeCount, lastSubarrays, buffer)

def GrailCombineInPlace(array:list, firstKey:int, start:int, length:int, subarrayLen:int, blockLen:int, mergeCount:int, lastSubarrays:int, buffer:bool) -> None:
    fullMerge:int = 2 * subarrayLen
    blockCount:int = fullMerge // blockLen

    for mergeIndex in range(mergeCount):
        offset:int = start + (mergeIndex * fullMerge)
        GrailInsertSort(array, firstKey, blockCount)
        medianKey:int = GrailBlockSelectSort(array, firstKey, offset, subarrayLen // blockLen, blockCount, blockLen)
        
        if buffer: GrailMergeBlocks(array, firstKey, firstKey + medianKey, offset, blockCount, blockLen, 0, 0)
        else: GrailLazyMergeBlocks(array, firstKey, firstKey + medianKey, offset, blockCount, blockLen, 0, 0)

    if lastSubarrays:
        offset:int = start + (mergeCount * fullMerge)
        blockCount:int = lastSubarrays // blockLen

        GrailInsertSort(array, firstKey, blockCount + 1)
        medianKey:int = GrailBlockSelectSort(array, firstKey, offset, subarrayLen // blockLen, blockCount, blockLen)

        lastFragment:int = lastSubarrays - (blockCount * blockLen)
        lastMergeBlocks:int = GrailCountLastMergeBlocks(array, offset, blockCount, blockLen) if lastFragment else 0
        smartMerges:int = blockCount - lastMergeBlocks

        if not smartMerges:
            leftLen:int = lastMergeBlocks * blockLen
            if buffer: GrailMergeForwards(array, offset, leftLen, lastFragment, blockLen)
            else: GrailLazyMerge(array, offset, leftLen, lastFragment)
        else:
            if buffer:
                GrailMergeBlocks(array, firstKey, firstKey + medianKey, offset, smartMerges, blockLen, lastMergeBlocks, lastFragment)
            else:
                GrailLazyMergeBlocks(array, firstKey, firstKey + medianKey, offset, smartMerges, blockLen, lastMergeBlocks, lastFragment)
    if buffer: GrailInPlaceBufferReset(array, start, length, blockLen)
   
def GrailCombineOutOfPlace(array:list, firstKey:int, start:int, length:int, subarrayLen:int, blockLen:int, mergeCount:int, lastSubarrays:int) -> None:
    ArrayCopy(array, start - blockLen, Grail.extBuffer, 0, blockLen)
    fullMerge:int = 2 * subarrayLen
    blockCount:int = fullMerge // blockLen

    for mergeIndex in range(mergeCount):
        offset:int = start + (mergeIndex * fullMerge)
        GrailInsertSort(array, firstKey, blockCount)
        medianKey:int = GrailBlockSelectSort(array, firstKey, offset, subarrayLen // blockLen, blockCount, blockLen)
        GrailMergeBlocksOutOfPlace(array, firstKey, firstKey + medianKey, offset, blockCount, blockLen, 0, 0)

    if lastSubarrays:
        offset:int = start + (mergeCount * fullMerge)
        blockCount:int = lastSubarrays // blockLen
        
        GrailInsertSort(array, firstKey, blockCount + 1)
        medianKey:int = GrailBlockSelectSort(array, firstKey, offset, subarrayLen // blockLen, blockCount, blockLen)

        lastFragment:int = lastSubarrays - (blockCount * blockLen)
        lastMergeBlocks:int = GrailCountLastMergeBlocks(array, offset, blockCount, blockLen) if lastFragment else 0
        smartMerges:int = blockCount - lastMergeBlocks

        if not smartMerges:
            leftLen:int = lastMergeBlocks * blockLen
            GrailMergeOutOfPlace(array, offset, leftLen, lastFragment, blockLen)
        else:
            GrailMergeBlocksOutOfPlace(array, firstKey, firstKey + medianKey, offset, smartMerges, blockLen, lastMergeBlocks, lastFragment)

    GrailOutOfPlaceBufferReset(array, start, length, blockLen)
    ArrayCopy(Grail.extBuffer, 0, array, start - blockLen, blockLen)

def GrailCommonSort(array:list, start:int, length:int, extBuffer:list=None, extBufferLen:int=None) -> None:
    if length < 16: return GrailInsertSort(array, start, length)
    blockLen:int = 1
    while blockLen ** 2 < length: blockLen *= 2

    keyLen:int = ((length - 1) // blockLen) + 1
    idealKeys:int = keyLen + blockLen
    keysFound:int = GrailCollectKeys(array, start, length, idealKeys)
    idealBuffer:bool = False

    if keysFound < idealKeys:
        if keysFound == 1: return
        if keysFound < 4: return GrailLazyStableSort(array, start, length)
        keyLen = blockLen
        blockLen = 0
        while keyLen > keysFound: keyLen //= 2
    else: idealBuffer = True

    bufferEnd:int = blockLen + keyLen
    subarrayLen:int = blockLen if idealBuffer else keyLen

    if idealBuffer and extBuffer:
        Grail.extBuffer = extBuffer
        Grail.extBufferLen = extBufferLen

    GrailBuildBlocks(array, start + bufferEnd, length - bufferEnd, subarrayLen)

    while length - bufferEnd > 2 * subarrayLen:
        subarrayLen *= 2
        currentBlockLen:int = blockLen
        scrollingBuffer:int = idealBuffer

        if not idealBuffer:
            keyBuffer = keyLen // 2
            if keyBuffer >= (2 * subarrayLen) // keyBuffer:
                currentBlockLen = keyBuffer
                scrollingBuffer = True
            else: currentBlockLen = (2 * subarrayLen) // keyLen

        GrailCombineBlocks(array, start, start + bufferEnd, length - bufferEnd, subarrayLen, currentBlockLen, scrollingBuffer)

    GrailInsertSort(array, start, bufferEnd)
    GrailLazyMerge(array, start, bufferEnd, length - bufferEnd)

    Grail.extBuffer = None
    Grail.extBufferLen = None

def GrailCountLastMergeBlocks(array:list, offset:int, blockCount:int, blockLen:int) -> int:
    blocksToMerge:int = 0
    lastRightFrag:int = offset + blockCount * blockLen
    prevLeftBlock:int = lastRightFrag - blockLen

    while blocksToMerge < blockCount and Compare(array[lastRightFrag], array[prevLeftBlock]) < 0:
        blocksToMerge += 1
        prevLeftBlock -= blockLen
    return blocksToMerge

def GrailGetSubarray(array:list, currentKey:int, medianKey:int) -> int:
    return LEFT if Compare(array[currentKey], array[medianKey]) < 0 else RIGHT

def GrailInPlaceBufferReset(array:list, start:int, length:int, bufferOffset:int) -> None:
    buffer:int = start + length - 1
    index:int = buffer - bufferOffset
    for i in range(buffer - start + 1): GrailSwap(array, index - i, buffer - i)

    # while buffer >= start:
    #     GrailSwap(array, index, buffer)
    #     buffer -= 1
    #     index -= 1

def GrailInPlaceBufferRewind(array:list, start:int, leftBlock:int, buffer:int) -> None:
    for i in range(leftBlock - start + 1): GrailSwap(array, buffer - i, leftBlock - i)
    # while leftBlock >= start:
    #     GrailSwap(array, buffer, leftBlock)
    #     buffer -= 1
    #     leftBlock -= 1

def GrailInsertSort(array:list, start:int, length:int) -> None:
    for item in range(1, length):
        left:int = start + item - 1
        right:Any = array[start + item]
        
        while left + 1 > start and Compare(array[left], right) > 0:
            array[left + 1] = array[left]
            left -= 1
        array[left + 1] = right
 
def GrailLazyMerge(array:list, start:int, leftLen:int, rightLen:int) -> None:
    if leftLen < rightLen:
        middle:int = start + leftLen
        while leftLen:
            mergeLen:int = GrailBinarySearchLeft(array, middle, rightLen, array[start])
            if mergeLen:
                GrailRotate(array, start, leftLen, mergeLen)
                start += mergeLen
                rightLen -= mergeLen
                middle += mergeLen

            if not rightLen: break
            
            while True:
                start += 1
                leftLen -= 1
                if not leftLen or Compare(array[start], array[middle]) > 0: break
    else:
        end:int = start + leftLen + rightLen - 1
        while rightLen:
            mergeLen:int = GrailBinarySearchRight(array, start, leftLen, array[end])
            if mergeLen != leftLen:
                GrailRotate(array, start + mergeLen, leftLen - mergeLen, rightLen)
                end -= leftLen - mergeLen
                leftLen = mergeLen

            if not leftLen: break

            middle:int = start + leftLen
            while True:
                rightLen -= 1
                end -= 1
                if not rightLen or Compare(array[middle - 1], array[end]) > 0: break
 
def GrailLazyMergeBlocks(array:list, firstKey:int, medianKey:int, start:int, blockCount:int, blockLen:int, lastMergeBlocks:int, lastLen:int) -> None:
    nextBlock:int = start + blockLen
    Grail.blockLen = blockLen
    Grail.blockOrigin = GrailGetSubarray(array, firstKey, medianKey)

    for index in range(1, blockCount):
        currBlock:int = nextBlock - Grail.blockLen
        nextBlockOrigin:int = GrailGetSubarray(array, firstKey + index, medianKey)

        if nextBlockOrigin == Grail.blockOrigin: Grail.blockLen = blockLen
        else: GrailSmartLazyMerge(array, currBlock, Grail.blockLen, Grail.blockOrigin, blockLen)
        nextBlock += blockLen
    
    currBlock:int = nextBlock - Grail.blockLen

    if lastLen:
        if Grail.blockOrigin == RIGHT:
            currBlock = nextBlock
            Grail.blockLen = blockLen * lastMergeBlocks
            Grail.blockOrigin = LEFT
        else: Grail.blockLen += blockLen * lastMergeBlocks        
        GrailLazyMerge(array, currBlock, Grail.blockLen, lastLen)

def GrailLazyStableSort(array:list, start:int, length:int) -> None:
    for index in range(1, length, 2):
        left:int = start + index - 1
        right:int = start + index

        if Compare(array[left], array[right]) > 0: GrailSwap(array, left, right)

    mergeLen:int = 2
    while mergeLen < length:
        fullMerge:int = 2 * mergeLen
        mergeEnd:int = length - fullMerge
        mergeIndex:int = 0

        while mergeIndex <= mergeEnd:
            GrailLazyMerge(array, start + mergeIndex, mergeLen, mergeLen)
            mergeIndex += fullMerge

        leftOver:int = length - mergeIndex
        if leftOver > mergeLen:
            GrailLazyMerge(array, start + mergeIndex, mergeLen, leftOver - mergeLen)
        mergeLen *= 2
 
def GrailMergeBackwards(array:list, start:int, leftLen:int, rightLen:int, bufferOffset:int) -> None:
    end:int = start - 1
    left:int = end + leftLen
    middle:int = left
    right:int = middle + rightLen
    buffer:int = right + bufferOffset
    while left > end:
        if right == middle or Compare(array[left], array[right]) > 0:
            GrailSwap(array, buffer, left)
            left -= 1
        else:
            GrailSwap(array, buffer, right)
            right -= 1
        buffer -= 1

    if right != buffer:
        for i in range(right - middle): GrailSwap(array, buffer - i, right - i)
        # while right > middle:
            # GrailSwap(array, buffer, right)
            # buffer -= 1
            # right -= 1

def GrailMergeBlocks(array:list, firstKey:int, medianKey:int, start:int, blockCount:int, blockLen:int, lastMergeBlocks:int, lastLen:int) -> None:
    nextBlock:int = start + blockLen
    Grail.blockLen:int = blockLen
    Grail.blockOrigin:int = GrailGetSubarray(array, firstKey, medianKey)

    for index in range(1, blockCount):
        currBlock:int = nextBlock - Grail.blockLen
        nextBlockOrigin:int = GrailGetSubarray(array, firstKey + index, medianKey)

        if nextBlockOrigin == Grail.blockOrigin:
            buffer:int = currBlock - blockLen
            GrailBlockSwap(array, buffer, currBlock, Grail.blockLen)
            Grail.blockLen = blockLen
        else:
            GrailSmartMerge(array, currBlock, Grail.blockLen, Grail.blockOrigin, blockLen, blockLen)

        nextBlock += blockLen
    
    currBlock:int = nextBlock - Grail.blockLen
    buffer:int = currBlock - blockLen

    if lastLen:
        if Grail.blockOrigin == RIGHT:
            GrailBlockSwap(array, buffer, currBlock, Grail.blockLen)
            currBlock = nextBlock
            Grail.blockLen = blockLen * lastMergeBlocks
            Grail.blockOrigin = LEFT
        else: Grail.blockLen += blockLen * lastMergeBlocks
        GrailMergeForwards(array, currBlock, Grail.blockLen, lastLen, blockLen)
    else: GrailBlockSwap(array, buffer, currBlock, Grail.blockLen)

def GrailMergeBlocksOutOfPlace(array:list, firstKey:int, medianKey:int, start:int, blockCount:int, blockLen:int, lastMergeBlocks:int, lastLen:int) -> None:
    nextBlock:int = start + blockLen
    Grail.blockLen:int = blockLen
    Grail.blockOrigin:int = GrailGetSubarray(array, firstKey, medianKey)

    for index in range(1, blockCount):
        currBlock:int = nextBlock - Grail.blockLen
        nextBlockOrigin:int = GrailGetSubarray(array, firstKey + index, medianKey)

        if nextBlockOrigin == Grail.blockOrigin:
            buffer:int = currBlock - blockLen
            ArrayCopy(array, currBlock, array, buffer, Grail.blockLen)
            Grail.blockLen = blockLen
        else:
            GrailSmartMergeOutOfPlace(array, currBlock, Grail.blockLen, Grail.blockOrigin, blockLen, blockLen)
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
        GrailMergeOutOfPlace(array, currBlock, Grail.blockLen, lastLen, blockLen)
    else: ArrayCopy(array, currBlock, array, buffer, Grail.blockLen)
 
def GrailMergeForwards(array:list, start:int, leftLen:int, rightLen:int, bufferOffset:int) -> None:
    left:int = start
    middle:int = start + leftLen
    right:int = middle
    end:int = middle + rightLen
    buffer:int = start - bufferOffset

    while right < end:
        if left == middle or Compare(array[left], array[right]) > 0:
            GrailSwap(array, buffer, right)
            right += 1
        else:
            GrailSwap(array, buffer, left)
            left += 1
        buffer += 1

    if buffer != left: GrailBlockSwap(array, buffer, left, middle - left)

def GrailMergeOutOfPlace(array:list, start:int, leftLen:int, rightLen:int, bufferOffset:int) -> None:
    left:int = start
    middle:int = start + leftLen
    right:int = middle
    end:int = middle + rightLen
    buffer:int = start - bufferOffset
    
    while right < end:
        if left == middle or Compare(array[left], array[right]) > 0:
            array[buffer] = array[right]
            right += 1
        else:
            array[buffer] = array[left]
            left += 1
        buffer += 1

    if buffer != left:
        for i in range(middle - left):
            array[buffer + i] = array[left + i]

def GrailOutOfPlaceBufferReset(array:list, start:int, length:int, bufferOffset:int) -> None:
    buffer:int = start + length - 1
    index:int = buffer - bufferOffset 

    for i in range(buffer - start + 1):
        array[buffer - i] = array[index - i]

def GrailOutOfPlaceBufferRewind(array:list, start:int, leftBlock:int, buffer:int) -> None:
    for i in range(leftBlock - start + 1):
        array[buffer - i] = array[leftBlock - i]

def GrailPairwiseSwaps(array:list, start:int, length:int) -> None:
    index:int = 1
    while index < length:
        left:int = start + index - 1
        right:int = start + index
        if Compare(array[left], array[right]) > 0:
            GrailSwap(array, left - 2, right)
            GrailSwap(array, right - 2, left)
        else:
            GrailSwap(array, left - 2, left)
            GrailSwap(array, right - 2, right)
        index += 2
    
    left:int = start + index - 1
    if left < start + length: GrailSwap(array, left - 2, left)

def GrailPairwiseWrites(array:list, start:int, length:int) -> None:
    index:int = 1
    while index < length:
        left:int = start + index - 1
        right:int = start + index

        if Compare(array[left], array[right]) > 0:
            array[left - 2], array[right - 2] = array[right], array[left]
        else:
            array[left - 2], array[right - 2] = array[left], array[right]
        index += 2

    left:int = start + index - 1
    if left < start + length: array[left - 2] = array[left]

def GrailRotate(array:list, start:int, leftLen:int, rightLen:int) -> None:
    while leftLen > 0 and rightLen > 0:
        if leftLen <= rightLen:
            GrailBlockSwap(array, start, start + leftLen, leftLen)
            start += leftLen
            rightLen -= leftLen
        else:
            GrailBlockSwap(array, start + leftLen - rightLen, start + leftLen, rightLen)
            leftLen -= rightLen

def GrailSmartLazyMerge(array:list, start:int, leftLen:int, leftOrigin:int, rightLen:int) -> None:
    middle:int = start + leftLen
    if leftOrigin == LEFT:
        if Compare(array[middle - 1], array[middle]) > 0:
            while leftLen:
                mergeLen:int = GrailBinarySearchLeft(array, middle, rightLen, array[start])
                if mergeLen:
                    GrailRotate(array, start, leftLen, mergeLen)
                    start += mergeLen
                    rightLen -= mergeLen
                    middle += mergeLen

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
                mergeLen:int = GrailBinarySearchRight(array, middle, rightLen, array[start])
                if mergeLen:
                    GrailRotate(array, start, leftLen, mergeLen)
                    start += mergeLen
                    rightLen -= mergeLen
                    middle += mergeLen

                if not rightLen:
                    Grail.blockLen = leftLen
                    return
                
                while True:
                    start += 1
                    leftLen -= 1
                    if not leftLen or Compare(array[start], array[middle]) >= 0: break

    Grail.blockLen = rightLen
    Grail.blockOrigin = RIGHT if leftOrigin == LEFT else LEFT

def GrailSmartMerge(array:list, start:int, leftLen:int, leftOrigin:int, rightLen:int, bufferOffset:int) -> None:
    left:int = start
    middle:int = start + leftLen
    right:int = middle
    end:int = middle + rightLen
    buffer:int = start - bufferOffset

    if leftOrigin == LEFT:
        while left < middle and right < end:
            if Compare(array[left], array[right]) < 1:
                GrailSwap(array, buffer, left)
                left += 1
            else:
                GrailSwap(array, buffer, right)
                right += 1
            buffer += 1
    else:
        while left < middle and right < end:
            if Compare(array[left], array[right]) < 0:
                GrailSwap(array, buffer, left)
                left += 1
            else:
                GrailSwap(array, buffer, right)
                right += 1
            buffer += 1

    if left < middle:
        Grail.blockLen = middle - left
        GrailInPlaceBufferRewind(array, left, middle - 1, end - 1)
    else:
        Grail.blockLen = end - right
        Grail.blockOrigin = RIGHT if leftOrigin == LEFT else LEFT

def GrailSmartMergeOutOfPlace(array:list, start:int, leftLen:int, leftOrigin:int, rightLen:int, bufferOffset:int) -> None:
    left:int = start
    middle:int = start + leftLen
    right:int = middle
    end:int = middle + rightLen
    buffer:int = start - bufferOffset

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
        Grail.blockLen = middle - left
        GrailOutOfPlaceBufferRewind(array, left, middle - 1, end - 1)
    else:
        Grail.blockLen = end - right
        Grail.blockOrigin = RIGHT if leftOrigin == LEFT else LEFT

def GrailSortDynamicBuffer(array:list, start:int, length:int) -> None:
    Grail.extBufferLen = 1
    while Grail.extBufferLen ** 2 < length: Grail.extBufferLen *= 2
    Grail.extBuffer = [0] * Grail.extBufferLen
    GrailCommonSort(array, start, length, Grail.extBuffer, Grail.extBufferLen)

def GrailSortInPlace(array:list, start:int, length:int) -> None:
    Grail.extBuffer = None
    Grail.extBufferLen = 0
    GrailCommonSort(array, start, length, None, 0)

def GrailSortStaticBuffer(array:list, start:int, length:int) -> None:
    Grail.extBuffer = [0] * GRAIL_STATIC_BUFFER_LEN
    Grail.extBufferLen = GRAIL_STATIC_BUFFER_LEN
    GrailCommonSort(array, start, length, Grail.extBuffer, GRAIL_STATIC_BUFFER_LEN)

def GrailSwap(array:list, a:int, b:int) -> None:
    array[a], array[b] = array[b], array[a]
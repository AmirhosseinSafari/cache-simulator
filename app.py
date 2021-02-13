import math
import datetime
import random
#----------------------------------------------------------------
#   Getting inputs from file
#----------------------------------------------------------------
def main():
    input_blocks = []

    input_file = open("input.txt", "r")
    line_counter = 0
    for line in input_file:
        line_counter += 1
        #print(line)
        if line_counter >= 9:
            input_blocks.append( int(line) )
            continue

        line = line.split(" ", 1)

        if line_counter == 1:
            cache_capacity:int = line[1]
            #TODO: validate input data and set an error after not valid input         
        if line_counter == 2:
            cache_structure = line[1]

        if line_counter == 3:
            block_size:int = line[1]

        if line_counter == 4:
            word_size:int = line[1]

        if line_counter == 5:
            replacement_method = line[1]

        if line_counter == 6:
            main_memory_capacity:int = line[1]

        if line_counter == 7:
            access_to_main_memory_method = line[1]
        
        if line_counter == 8:
            n:int = line[1]
            #TODO: validate input data and set an error after not valid input

        #------------- list of input vars -------------
        #   cache_capacity
        #   cache_structure
        #   block_size
        #   word_size
        #   replacement_method
        #   main_memory_capacity
        #   access_to_main_memory_method
    
    print(input_blocks)
    #----------------------------------------------------------------
    #   common computed data
    #----------------------------------------------------------------

    main_memory_blocks_count:int = int(main_memory_capacity) / int(block_size)
    cache_blocks_count:int =  int(cache_capacity) / int(block_size)
    bits_of_main_mem_address:int =  math.log( int(main_memory_capacity), 2 )
    bits_of_cache_address:int = math.log( int(cache_capacity), 2 )
    bits_of_byte_offset:int = math.log( int(block_size),2 )

    cache = [["MPT" for j in range( int(block_size) )] for i in range( int(cache_blocks_count) )]        
    max_block_number = ( int(block_size) * int(main_memory_blocks_count) ) - 1  
    #----------------------------------------------------------------
    #   cache structures
    #----------------------------------------------------------------

    if str(cache_structure) == "direct\n":                              #<<----------------- direct map

        bits_of_index_direct_map = math.log( cache_blocks_count,2 )
        bits_of_tag_direct_map:int = bits_of_main_mem_address - ( bits_of_byte_offset + bits_of_index_direct_map )
        tag_stuff = [["EMT" for j in range( int(bits_of_tag_direct_map) + 1 )] for i in range( int(cache_blocks_count) )]    #tag + valid bit array

        for i in range(int(cache_blocks_count)):                        #initialing by EMT and 0 for valid bit
            tag_stuff[i][int(bits_of_tag_direct_map) + 1 - 1] = 0

        #cache_printer( cache, tag_stuff, cache_blocks_count )

        for request_blk in input_blocks:
            
            if request_blk > max_block_number:
                print("\n###############################")
                print("this address can't exist in cache; it's greater than maximum block address")
                continue

            binary = decimal_to_bin( int(request_blk), bits_of_main_mem_address )
            index_direct_map_binary = binary[int(bits_of_byte_offset): int( bits_of_index_direct_map + bits_of_byte_offset)]

            index_direct_map_decimal = bin_to_decimal(index_direct_map_binary)
            
            #---------------------------------------------
            #   check if hit
            #---------------------------------------------

            if  tag_stuff[ index_direct_map_decimal ][ int(bits_of_tag_direct_map) + 1 - 1 ] == 1:
                hit_flage = True
                i = int(bits_of_tag_direct_map) - 1
                j = 0
                while i >= 0:
                    if tag_stuff[index_direct_map_decimal][i] != int(binary[j + int(bits_of_byte_offset) + int(bits_of_index_direct_map)]):
                        hit_flage = False
                        break
                    i -= 1
                    j+= 1
            else: 
                hit_flage = False

            #print(hit_flage)
            #---------------------------------------------
            #   if not hit (miss)
            #---------------------------------------------   
            if hit_flage == False:

                first_of_block = first_block_number(request_blk, block_size)
                for i in range( int(block_size) ):
                    cache[index_direct_map_decimal][i] = first_of_block + i

                i = int(bits_of_tag_direct_map) - 1
                j = 0
                #print(binary)
                while i >= 0:
                    tag_stuff[index_direct_map_decimal][i] = int(binary[j + int(bits_of_byte_offset) + int(bits_of_index_direct_map)])
                    i -= 1
                    j += 1

                tag_stuff[index_direct_map_decimal][int(bits_of_tag_direct_map) + 1 - 1] = 1       #valid bit = 1

                print("\n##########################")
                print("It was a miss for address byte " + str(request_blk) + "\n")
                cache_printer( cache, tag_stuff, cache_blocks_count )
            
            #---------------------------------------------
            #   if hit
            #---------------------------------------------
            else:
                print("\n##########################")
                print("It was a Hit for address byte " + str(request_blk) + "\n")
                cache_printer( cache, tag_stuff, cache_blocks_count )

            
    if cache_structure == "n-way\n":                                #<<----------------- n-way

        bits_of_index_n_way = math.log( int(cache_blocks_count)/int(n) ,2 )
        bits_of_tag_n_way:int = bits_of_main_mem_address - ( bits_of_byte_offset + bits_of_index_n_way )
        tag_stuff = [["EMT" for j in range( int(bits_of_tag_n_way) + 1 )] for i in range( int(cache_blocks_count) )]    #tag + valid bit array
        age_counter = [ 0 for i in range( int(cache_blocks_count) ) ]
        used_times = [ 0 for i in range( int(cache_blocks_count) ) ]
        fifo = [ 0 for i in range( int(cache_blocks_count) ) ]

        for i in range(int(cache_blocks_count)):                        #initialing by EMT and 0 for valid bit
            tag_stuff[i][int(bits_of_tag_n_way) + 1 - 1] = 0

        for request_blk in input_blocks:
            
            if request_blk > max_block_number:
                print("\n###############################")
                print("this address can't exist in cache; it's greater than maximum block address")
                continue
        
            binary = decimal_to_bin( int(request_blk), bits_of_main_mem_address )
            index_n_way_binary = binary[int(bits_of_byte_offset): int( bits_of_index_n_way + bits_of_byte_offset)]

            index_n_way_decimal = bin_to_decimal(index_n_way_binary)

            #print(index_n_way_binary)
            #---------------------------------------------
            #   check if hit
            #---------------------------------------------

            for i in range( int(n) ):
                if tag_stuff[ int(index_n_way_decimal) * int(n) + i ][ int(bits_of_tag_n_way) ] == 1:
                    hit_flage = True
                    i1 = int(bits_of_tag_n_way) - 1
                    j = 0
                    while i1 >= 0:
                        if tag_stuff[ index_n_way_decimal * int(n) + i ][i1] != int(binary[j + int(bits_of_byte_offset) + int(bits_of_index_n_way)]):
                            hit_flage = False
                            break
                        i1 -= 1
                        j+= 1
                else:
                    hit_flage = False 

                if hit_flage == True:
                    break
            
            #---------------------------------------------
            #   if not hit (miss)
            #---------------------------------------------   
            if hit_flage == False:

                if replacement_method == "LRU\n":
                    replacement_method_num = LRU_method(tag_stuff, age_counter, index_n_way_decimal, n)

                if replacement_method == "random\n":
                    replacement_method_num = random_method(tag_stuff, index_n_way_decimal, n)

                if replacement_method == "LFU\n":
                    replacement_method_num = LFU_method(tag_stuff, used_times, index_n_way_decimal, n)

                if replacement_method == "FIFO\n":
                    replacement_method_num = FIFO_method(tag_stuff, fifo, index_n_way_decimal, n)
                
                #print(replacement_method_num)
                tag_stuff[ index_n_way_decimal * int(n) + replacement_method_num ][ int(bits_of_tag_n_way)] = 1
                
                first_of_block = first_block_number(request_blk, block_size)
                for i in range( int(block_size) ):
                    cache[index_n_way_decimal * int(n) + replacement_method_num][i] = first_of_block + i

                i = int(bits_of_tag_n_way) - 1
                j = 0
                #print(binary)
                while i >= 0:
                    tag_stuff[index_n_way_decimal * int(n) + replacement_method_num][i] = int(binary[j + int(bits_of_byte_offset) + int(bits_of_index_n_way)])
                    i -= 1
                    j += 1

                tag_stuff[ index_n_way_decimal * int(n) + replacement_method_num ][int(bits_of_tag_n_way)] = 1   #valid bit

                print("\n##########################")
                print("It was a miss for address byte " + str(request_blk) + "\n")
                cache_printer( cache, tag_stuff, cache_blocks_count )
            
            #---------------------------------------------
            #   if hit
            #---------------------------------------------
            else:
                used_times[index_n_way_decimal * int(n) + replacement_method_num] += 1
                age_counter[index_n_way_decimal * int(n) + replacement_method_num] = datetime.datetime.now()

                print("\n##########################")
                print("It was a Hit for address byte " + str(request_blk) + "\n")
                cache_printer( cache, tag_stuff, cache_blocks_count )


    if cache_structure == "fully\n":
        
        bits_of_tag_fully:int = bits_of_main_mem_address - ( bits_of_byte_offset )
        tag_stuff = [["EMT" for j in range( int(bits_of_tag_fully) + 1 )] for i in range( int(cache_blocks_count) )]    #tag + valid bit array
        age_counter = [ 0 for i in range( int(cache_blocks_count) ) ]
        used_times = [ 0 for i in range( int(cache_blocks_count) ) ]
        fifo = [ 0 for i in range( int(cache_blocks_count) ) ]

        for i in range(int(cache_blocks_count)):                        #initialing by EMT and 0 for valid bit
            tag_stuff[i][int(bits_of_tag_fully) + 1 - 1] = 0

        for request_blk in input_blocks:
            
            if request_blk > max_block_number:
                print("\n###############################")
                print("this address can't exist in cache; it's greater than maximum block address")
                continue
                
            binary = decimal_to_bin( int(request_blk), bits_of_main_mem_address )
        
            #---------------------------------------------
            #   check if hit
            #---------------------------------------------
            for i in range( int(cache_blocks_count) ):
                if tag_stuff[ i ][ int(bits_of_tag_fully) ] == 1:
                    hit_flage = True
                    i1 = int(bits_of_tag_fully) - 1
                    j = 0
                    while i1 >= 0:
                        if tag_stuff[ i ][i1] != int(binary[j + int(bits_of_byte_offset)]):
                            hit_flage = False
                            break
                        i1 -= 1
                        j+= 1
                else:
                    hit_flage = False 

                if hit_flage == True:
                    break  
        
            #---------------------------------------------
            #   if not hit (miss)
            #---------------------------------------------   
            if hit_flage == False:

                if replacement_method == "LRU\n":
                    replacement_method_num = LRU_method(tag_stuff, age_counter, 0, int(cache_blocks_count) )

                if replacement_method == "random\n":
                    replacement_method_num = random_method(tag_stuff, 0, int(cache_blocks_count) )

                if replacement_method == "LFU\n":
                    replacement_method_num = LFU_method(tag_stuff, used_times, 0, int(cache_blocks_count) )

                if replacement_method == "FIFO\n":
                    replacement_method_num = FIFO_method(tag_stuff, fifo, 0, int(cache_blocks_count) )

                #print(replacement_method_num)
                tag_stuff[ replacement_method_num ][ int(bits_of_tag_fully)] = 1
                
                first_of_block = first_block_number(request_blk, block_size)
                for i in range( int(block_size) ):
                    cache[replacement_method_num][i] = first_of_block + i

                i = int(bits_of_tag_fully) - 1
                j = 0
                #print(binary)
                while i >= 0:
                    tag_stuff[replacement_method_num][i] = int(binary[j + int(bits_of_byte_offset)])
                    i -= 1
                    j += 1

                tag_stuff[ replacement_method_num ][int(bits_of_tag_fully)] = 1   #valid bit

                print("\n##########################")
                print("It was a miss for address byte " + str(request_blk) + "\n")
                cache_printer( cache, tag_stuff, cache_blocks_count )
            
            #---------------------------------------------
            #   if hit
            #---------------------------------------------
            else:
                used_times[replacement_method_num] += 1
                age_counter[replacement_method_num] = datetime.datetime.now()

                print("\n##########################")
                print("It was a Hit for address byte " + str(request_blk) + "\n")
                cache_printer( cache, tag_stuff, cache_blocks_count )
        #print(  )


def decimal_to_bin(decimal, length):
        binary_num:str = ""
        while(decimal != 0):
            binary_num = binary_num + str(decimal % 2)
            decimal = int(decimal/2)
        
        for i in range( int (length - len(binary_num)) ):
            binary_num += "0"

        return binary_num

def first_block_number(num, block_size):
    first_number_of_block:int

    for i in range(int(block_size)):
        if num % int(block_size) == 0:
            first_number_of_block = num
            break
        else:
            num -= 1
    
    return first_number_of_block

def bin_to_decimal(bin_num):
        decimal = 0
        i = 0
        for b in bin_num:
            decimal += int(b)*2**i
            i+=1
        return decimal

def LRU_method(tag_stuff, age_counter, index_decimal, n):
    for i in range( int(n) ):
        if tag_stuff[index_decimal * int(n) + i][-1] == 0:
            replace_num = i
            age_counter[index_decimal * int(n) + replace_num] = datetime.datetime.now()
            return replace_num
    
    LRU_index = -1
    older: datetime.datetime
    #print("----------------> " + str(LRU_index))
    #print(age_counter)
    for i in range( int(n) ):
        
        if LRU_index == -1:
           older = age_counter[index_decimal * int(n) ]
           LRU_index = i
        
        if age_counter[index_decimal * int(n) + i] < older:
            older = age_counter[index_decimal * int(n) + i]
            LRU_index = i
    
    age_counter[index_decimal * int(n) + LRU_index] = datetime.datetime.now()
    return LRU_index

def random_method(tag_stuff, index_decimal, n):

    for i in range( int(n) ):
        if tag_stuff[index_decimal * int(n) + i][-1] == 0:
            replace_num = i
            return replace_num

    replace_num = random.randint(0,  int(n)-1)
    return replace_num

def LFU_method(tag_stuff, used_times, index_decimal, n):

    for i in range( int(n) ):
        if tag_stuff[index_decimal * int(n) + i][-1] == 0:
            replace_num = i
            used_times[index_decimal * int(n) + replace_num] += 1 
            return replace_num
    
    LFU_index = -1
    for i in range( int(n) ):
        
        if LFU_index == -1:
           less_used = used_times[index_decimal * int(n) ]
           LFU_index = i
        
        if used_times[index_decimal * int(n) + i] < less_used:
            less_used = used_times[index_decimal * int(n) + i]
            LFU_index = i
    
    used_times[index_decimal * int(n) + LFU_index] = 1
    return LFU_index


def FIFO_method(tag_stuff, fifo, index_decimal, n):

    for i in range( int(n) ):
        if tag_stuff[index_decimal * int(n) + i][-1] == 0:
            replace_num = i
            fifo[index_decimal * int(n) + i] = datetime.datetime.now()
            return replace_num
    
    first_in = -1
    first_in_index = -1
    for i in range( int(n) ):

        if first_in == -1:
            first_in = fifo[ index_decimal* int(n) ]
            first_in_index = i

        if  fifo[ index_decimal* int(n) + i] < first_in:
            first_in = fifo[ index_decimal* int(n) + i]
            first_in_index = i

    fifo[ index_decimal* int(n) + first_in_index] = datetime.datetime.now()
    return first_in_index


def cache_printer(matrix1, matrix2, height):
    for i in range( int(height) ):
        print(str(matrix1[i]) + " " + str(matrix2[i]) )

if __name__ == "__main__":
    main()
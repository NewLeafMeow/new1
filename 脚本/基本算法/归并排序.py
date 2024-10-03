def merge_sort(arr):
    if len(arr) > 1:
        # 找到数组的中间点
        mid = len(arr) // 2
        
        # 拆分数组为两个子数组
        left_half = arr[:mid]
        right_half = arr[mid:]
        
        # 递归地对每个子数组进行排序
        merge_sort(left_half)
        merge_sort(right_half)
        
        # 初始化三个指针，i用于遍历left_half, j用于遍历right_half, k用于重建arr
        i = j = k = 0
        
        # 合并两个子数组
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1
        
        # 检查任何剩余的元素
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1
        
        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

# 测试
arr = [38, 27, 43, 3, 9, 82, 10]
print("原数组:", arr)
merge_sort(arr)
print("排序后数组:", arr)

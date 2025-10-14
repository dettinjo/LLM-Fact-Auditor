def longest_common_substring(s1, s2):
    dp = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]
    max_length = 0 
    end_pos = 0 

    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > max_length:
                    max_length = dp[i][j]
                    end_pos = i

    lcs = s1[end_pos - max_length:end_pos]
    return max_length, lcs

if __name__ == "__main__":
    print(longest_common_substring(" not","England"))
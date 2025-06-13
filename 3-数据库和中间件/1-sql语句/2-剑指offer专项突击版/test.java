class Solution {
    public boolean validPalindrome(String s) {
        int n = s.length();
        int left = 0, right = n - 1;
        while (left < right) {
            if (++left == --right){
                return true;
            }
            if ((s.charAt(left) != s.charAt(right)) && (s.charAt(++left) != s.charAt(right)) && (s.charAt(left) != s.charAt(--right))) {
                return false;
            }
            ++left;
            --right;
        }
        return true;
    }
}
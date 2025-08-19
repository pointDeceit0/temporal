#include <vector>

/** @brief PAV - pool adjacent violators algorithm
 * 
 * PAV is well known algorithm of making the sequnce stepwise.
 * The implementation PAV is a key of using C++, becuase its requirement in nested loops.
 * 
 * @param input the initial sequence that PAVa will be applied
 * @return PAVed sequence
 */
std::vector<long double> pav(const std::vector<long double>& input);


std::vector<long double> pav(const std::vector<long double>& input) {
    size_t n = input.size();
    if (n == 0) return {};

    std::vector<long double> values = input;
    std::vector<int> sizes(n, 1);
    size_t i = 0;

    for (size_t j = 1; j < n; ++j) {
        values[++i] = input[j];
        sizes[i] = 1;

        // goes till the moment all following elements are less or equal of current
        while (i > 0 && values[i - 1] > values[i]) {
            long double total = values[i - 1] * sizes[i - 1] + values[i] * sizes[i];
            sizes[i - 1] += sizes[i];
            values[i - 1] = total / sizes[i - 1];
            --i;
        }
    }

    // writing in result vector
    std::vector<long double> result;
    for (size_t j = 0; j <= i; ++j) {
        result.insert(result.end(), sizes[j], values[j]);
    }

    return result;
}

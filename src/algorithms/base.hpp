#include <vector>
#include <numeric>

/** @brief Returns mean of the passed array of numbers
 *
 *  @param v the vector that mean of should be calculated
 *  @return The mean of given number sequence
 */
long double mean(const std::vector<long double>& v);


long double mean(const std::vector<long double>& v) {
    if (v.empty()) return 0.0;
    return std::accumulate(v.begin(), v.end(), 0.0) / v.size();
}
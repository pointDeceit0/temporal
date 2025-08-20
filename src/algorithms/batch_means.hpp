#include <vector>
#include <numeric>

/** @brief Making batch means procedure to the given sequence
 * 
 * The batch mean procedure is known procedure of autocorrelation descreasing by merging groups of elements
 * and replacing them with theirs mean. The procedure allows to decrease sequence autocorrelation significantly
 * 
 * @param data the initial sequence that batch mean should be applied on
 * @param size the size of batch
 * @return The result sequence after batch mean
 */
std::vector<long double> batch_means(const std::vector<long double>& data, int size);


std::vector<long double> batch_means(const std::vector<long double>& data, int size) {
    std::vector<long double> means;

    for (size_t i = size; i <= data.size(); i += size) {
        long double sum = std::accumulate(data.begin() + (i - size), data.begin() + i, 0.0);
        means.push_back(sum / size);
    }

    return means;
}
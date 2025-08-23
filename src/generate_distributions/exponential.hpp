#include <vector>
#include <random>


// generates exponent distributed sample
std::vector<long double> generate_exponential(long double lambda, int n, std::mt19937& gen) {
    std::exponential_distribution<long double> dist(lambda);
    std::vector<long double> result(n);
    for (int i = 0; i < n; ++i) result[i] = dist(gen);
    return result;
}
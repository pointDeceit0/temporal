#include <vector>
#include <cmath>
#include <iomanip> 
#include <numeric>
#include <fstream>
#include "src/algorithms/pav.hpp"
#include "src/algorithms/base.hpp"
#include <boost/math/distributions/normal.hpp>
#include <boost/math/distributions/beta.hpp>

/** @brief Standard deviation calculation of normal approximation of Stirling numbers of first kind
 * 
 * There's exists well-known approximation of Stirling numbers of first kind that looks like normal approximation
 * with following parameters:
 * 
 * \mu = log N - mean,
 * \sigma = H_N^{(1)} - H_N^{(2)} - standard deviation,
 * 
 * where N is the sample size (N -> \infty), H_N^{(1)} - i-th order harmonic number (i = 1, 2)
 * 
 * @param n the sample size
 * @return Computed standard deviation of normal approximation
 */
long double compute_sd_sum(int n);

/** @brief amt CDF calculated with normal approximation
 * 
 * CDF of amt calculated with normal approximation.
 * More information could be founded on main page of the project on github
 * 
 * @param n the sample size
 * @param e the statistics value
 * @return The number between 0 and 1, the resulting probability
 */
long double amt_cdf_approximated_normal(int n, long double e);

/** @brief Statistics calculating of AMT method 
 * 
 * Statistics calculating of amt method.
 * More information could be founded on main page of the project on github
 * 
 * @param pav the PAVed initial sequence (pav of raw)
 * @param raw the initial sequence
 * @return statistics of using method amt
*/
long double e_bar_statistic(const std::vector<long double>& pav, const std::vector<long double>& raw);

/** @brief Calculating of p-value of Analysis of Monotone Trend method 
 * 
 * Calculating of p-value of Analysis of Monotone Trend method.
 * More information could be founded on main page of the project on github
 * 
 * @param a the exploring sequence
 * @return p-value 
*/
long double amt(std::vector<long double>& a);


long double compute_sd_sum(int n) {
    long double sum = 0.0;
    for (int i = 1; i < n; ++i) {  // using harmonic numbers
        sum += (1.0 / (long double)i) - (1.0 / (long double)(i * i));
    }
    return sqrt(sum);
}


long double amt_cdf_approximated_normal(int n, long double e) {
    if (n < 2) throw std::invalid_argument("n must be at least 2");

    // parameter of normal distribution
    long double mean = log(n);
    long double sd = compute_sd_sum(n);

    boost::math::normal_distribution<long double> norm_dist(mean, sd);

    long double total = 0.0;
    int max_i = static_cast<int>(4 * log(n));

    for (int i = 2; i < std::min(max_i, n); ++i) {
        boost::math::beta_distribution<long double> beta_dist((i - 1.0) / 2.0, (n - i) / 2.0);
        long double normal_pdf = pdf(norm_dist, i);
        long double beta_cdf = cdf(beta_dist, e);
        total += normal_pdf * beta_cdf;
    }

    return total + 1.0 / n;
}


long double e_bar_statistic(const std::vector<long double>& pav, const std::vector<long double>& raw) {
    if (pav.size() != raw.size()) {
        throw std::invalid_argument("Vectors must be of the same size.");
    }

    long double raw_mean = mean(raw);
    long double numerator = 0.0;
    long double denominator = 0.0;

    for (size_t i = 0; i < pav.size(); ++i) {
        numerator += pow(pav[i] - raw_mean, 2);
        denominator += pow(raw[i] - raw_mean, 2);
    }

    if (denominator == 0.0) {
        throw std::runtime_error("Denominator is zero, cannot divide.");
    }

    return numerator / denominator;
}


long double amt(std::vector<long double>& a) {
    long double statistic = e_bar_statistic(pav(a), a);

    return 1 - amt_cdf_approximated_normal(a.size(), statistic);
}
#include <iostream>
#include <vector>
#include "src/algorithms/batch_means.hpp"
#include <src/amt/amt.hpp>

/** @brief Gets number sequence and launches Analys of Monotone Trend test for that
 * 
 * The main purpose of this file and function in this file to read data from pipe (in particular case using
 * subprocess and PIPI from that in python) and implement AMT test for that and then return result for given sequence.
 * 
 * All errors handlers must be placed in python code (due to my bad c++))).
 * 
 * It is also assumed that (in particular case of current state of application) python uses complied file for using.
 */
int main(int argc, char* argv[]) {
    std::vector<long double> data;
    long double val;
    while(std::cin.read(reinterpret_cast<char*>(&val), sizeof(long double))) {
        data.push_back(val);
    }

    // reading of batch size in argv 1
    auto a = batch_means(data, (int)std::stoi(argv[1]));
    // handle it from python code
    std::cout << amt(a) << std::endl;
    return 0;
}
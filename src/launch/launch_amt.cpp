#include <iostream>
#include <vector>
#include "src/algorithms/batch_means.hpp"
// #include "src/algorithms/pav.hpp"
#include "src/amt/amt.hpp"


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

    const char* input_filename = argv[1];
    const char* output_filename = argv[2];
    int batch_size = std::stoi(argv[3]);  // string to integer
    std::vector<long double> data;

    try {
        std::ifstream input_file(input_filename, std::ios::binary | std::ios::ate);  // till the end
        if (!input_file) {
            throw std::runtime_error("Cannot open input file: " + std::string(input_filename));
        }
        
        std::streamsize file_size = input_file.tellg();
        input_file.seekg(0, std::ios::beg);
        
        if (file_size % sizeof(float) != 0) {
            std::cerr << "Warning: input file size not multiple of float size" << std::endl;
        }
        
        // number of entries in file
        size_t num = file_size / sizeof(float);
        data.reserve(num);

        std::vector<char> buffer(file_size);
        if (!input_file.read(buffer.data(), file_size)) {  // reading of temp file
            throw std::runtime_error("Cannot read input file");
        }
        input_file.close();
        
        // conversion to long doupble
        for (size_t i = 0; i < num; ++i) {
            float val;
            // copying to the val from buffer based on the size of float
            std::memcpy(&val, &buffer[i * sizeof(float)], sizeof(float));
            data.push_back(static_cast<long double>(val));
        }
        
        // Обработка данных
        auto batched = batch_means(data, batch_size);
        auto paved = pav(batched);
        double amt_result = amt(batched, paved);
        
        // writing in output file
        std::ofstream output_file(output_filename);
        if (!output_file) {
            throw std::runtime_error("Cannot open output file: " + std::string(output_filename));
        }
        // writing AMT result
        output_file << amt_result << "\n";
        // writing result of paved inition array
        for (int i = 0; i < paved.size(); i++) {
            output_file << paved[i] << " ";
        }
        std::cout << "\n";
        
        output_file.close();
        return 0;
    } catch (const std::exception& e) {
        // writing error into output file if smth went wrong
        std::ofstream output_file(output_filename);
        if (output_file) {
            output_file << "ERROR: " << e.what() << std::endl;
        }
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
}
# NoLiMa: Long-Context Evaluation Beyond Literal Matching

This repository contains the code and data associated with our paper, "[NoLiMa: Long-Context Evaluation Beyond Literal Matching](https://arxiv.org/abs/2502.05167)".

## Abstract
> Recent large language models (LLMs) support long contexts ranging from 128K to 1M tokens. A popular method for evaluating these capabilities is the needle-in-a-haystack (NIAH) test, which involves retrieving a "needle" (relevant information) from a "haystack" (long irrelevant context). Extensions of this approach include increasing distractors, fact chaining, and in-context reasoning. However, in these benchmarks, models can exploit existing literal matches between the needle and haystack to simplify the task. To address this, we introduce **NoLiMa**, a benchmark extending NIAH with a carefully designed needle set, where questions and needles have **minimal lexical overlap, requiring models to infer latent associations to locate the needle within the haystack**. We evaluate 12 popular LLMs that claim to support contexts of at least 128K tokens. While they perform well in short contexts ($<$1K), performance degrades significantly as context length increases. At 32K, for instance, 10 models drop below 50\% of their strong short-length baselines. Even GPT-4o, one of the top-performing exceptions, experiences a reduction from an almost-perfect baseline of 99.3\% to 69.7\%. Our analysis suggests these declines stem from the increased difficulty the attention mechanism faces in longer contexts when literal matches are absent, making it harder to retrieve relevant information.

## Results
| Models               | Claimed Length | Effective Length | Base Score<br>(×0.85: Thr.) | 1K  | 2K  | 4K  | 8K  | 16K | 32K |
|----------------------|:-------------:|:---------------:|:-----------------------:|:---:|:---:|:---:|:---:|:---:|:---:|
| GPT-4o              | 128K          | 8K              | 99.3 (84.4)             | <ins>98.1</ins> | <ins>98.0</ins> | <ins>95.7</ins> | <ins>89.2</ins> | 81.6 | 69.7 |
| Llama 3.3 70B       | 128K          | 2K              | 97.3 (82.7)             | <ins>94.2</ins> | <ins>87.4</ins> | 81.5 | 72.1 | 59.5 | *42.7* |
| Llama 3.1 405B      | 128K          | 2K              | 94.7 (80.5)             | <ins>89.0</ins> | <ins>85.0</ins> | 74.5 | 60.1 | 48.4 | *38.0* |
| Llama 3.1 70B       | 128K          | 2K              | 94.5 (80.3)             | <ins>91.0</ins> | <ins>81.8</ins> | 71.2 | 62.7 | 51.8 | *43.2* |
| Gemini 1.5 Pro      | 2M            | 2K              | 92.6 (78.7)             | <ins>86.4</ins> | <ins>82.7</ins> | 75.4 | 63.9 | 55.5 | 48.2 |
| Jamba 1.5 Mini      | 256K          | <1K             | 92.4 (78.6)             | 76.3 | 74.1 | 70.8 | 62.2 | 52.7 | *43.6* |
| Command R+          | 128K          | <1K             | 90.9 (77.3)             | 77.0 | 73.5 | 66.3 | *39.5* | *21.3* | *7.4* |
| Mistral Large 2     | 128K          | 2K              | 87.9 (74.7)             | <ins>86.1</ins> | <ins>85.5</ins> | 73.3 | 51.5 | *32.6* | *18.7* |
| Claude 3.5 Sonnet   | 200K          | 4K              | 87.6 (74.4)             | <ins>85.4</ins> | <ins>84.0</ins> | <ins>77.6</ins> | 61.7 | 45.7 | *29.8* |
| Gemini 1.5 Flash    | 1M            | <1K             | 84.7 (72.0)             | 68.6 | 61.6 | 51.0 | 44.4 | *35.5* | *28.6* |
| GPT-4o mini         | 128K          | <1K             | 84.9 (72.2)             | 67.7 | 58.2 | 44.1 | *32.6* | *20.6* | *13.7* |
| Llama 3.1 8B        | 128K          | 1K              | 76.7 (65.2)             | <ins>65.7</ins> | 54.4 | 44.1 | *31.9* | *22.6* | *14.2* |

This table presents the performance results of selected models on NOLIMA tests. The **base score** represents a model’s accuracy on the task at short contexts (250, 500, and 1K) and serves as a controlled reference to measure performance degradation at longer contexts. 
The **effective length** is defined as the longest context where a model maintains at least 85% of its base score. Scores above this threshold are <ins>underlined</ins>, while scores dropping below 50% of the base score are *italicized*.

### NoLiMa-Hard Results
| Models                | Base Score | 4K  | 8K  | 16K | 32K |
|-----------------------|:---------:|:---:|:---:|:---:|:---:|
| **Llama 3.3 70B**     |           |     |     |     |     |
| - w/o CoT            | 98.3       | 55.5 | *37.2* | *16.7* | *8.9* |
| - w/ CoT             | 97.1       | 73.0 | 51.2 | *31.8* | *10.1* |
| **Reasoning Models**  |           |     |     |     |     |
| GPT-o1               | 99.9       | 92.0 | 78.0 | 60.1 | *31.1* |
| GPT-o3 Mini          | 98.8       | 52.8 | *36.9* | *25.5* | *18.9* |
| DeepSeek R1-Distill-Llama-70B   | 99.9       | 91.4 | 75.5 | *49.4* | *20.7* |

This table presents the performance results of selected reasoning models on **NoLiMa-Hard**, a subset of the original NoLiMa needle set containing the 10 most challenging question-needle pairs from previous evaluations. 
Scores dropping below 50% of the base score are in *italic*.


## Model Evaluation Instructions

Below are the general steps to evaluate models, whether serving them locally or using an API-based service.

---
### 1. Installing Requirements
Install the required packages by running:
```bash
pip install -r requirements.txt
```

### 2. Downloading Data
Download the NoLiMa dataset by running:
```bash
data/download_NoLiMa_data.sh
```
The needle set and haystack data will be downloaded to the `data` directory from our [HuggingFace Datasets 🤗](https://huggingface.co/datasets/amodaresi/NoLiMa) repository.

### 3A. Locally Served Models

1. **Start the model server (optional)**  
   - For example, to serve the Meta Llama 3.3 (70B) model across 8 GPUs:  
     ```bash
     evaluation/vllm_serve.sh --model_name meta-llama/Llama-3.3-70B-Instruct --num_gpus 8
     ```
   - This script uses a tensor parallel configuration by default. Modify it as needed.

2. **Create or modify a local model configuration**  
   - Use `llama_3.3_70b.json` in the `evaluation/model_configs` folder as a reference.
   Note that this configuration file is used in the evaluation script (not for the vllm serve).

### 3B. API-Based Models

- **Create or modify a model configuration for your API-based service**  
  - For example, use the existing config templates in the `evaluation/model_configs` folder.  
  - Note that some APIs may require additional credentials or authentication (AWS, Google Auth, etc.).

### 4. Common Steps for Both Approaches

1. **Prepare test configuration files**  
   - Add or modify configuration files in the `evaluation/run_config` directory.  
   - Ensure they reference the correct model config file from `evaluation/model_configs`.

2. **Run the evaluations**  
   ```bash
   evaluation/run_tests.sh
   ```
3. **Collect the results**
    - All outputs are automatically saved to the results directory specified in each run_config file.
4. **Gathering the results**
    - Using the `evaluation/gather_results.ipynb` notebook, you can easily gather the results from the output files and generate a csv file containing the accuracy of each test.

### Additional Notes
You can find various needle sets (e.g., CoT-style, multiple choice, direct, distractor-included) in `data/needlesets`.
Adjust any paths or configurations as needed for your specific environment.

---

## Haystack Filtering Pipeline

To replicate our evaluation results, you can directly use the shuffled texts available in the `data/haystack/rand_shuffle` directory. If you prefer to generate your own shuffled texts or run the full processing pipeline from scratch, refer to the `data/README.md` file for more information.

## Cite
If you use the **NoLiMa** dataset, filtering pipeline, or code from this repository, please cite the paper:
```bibtex
@misc{modarressi2025nolimalongcontextevaluationliteral,
      title={NoLiMa: Long-Context Evaluation Beyond Literal Matching}, 
      author={Ali Modarressi and Hanieh Deilamsalehy and Franck Dernoncourt and Trung Bui and Ryan A. Rossi and Seunghyun Yoon and Hinrich Schütze},
      year={2025},
      eprint={2502.05167},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2502.05167}, 
}
```

## License

The evaluation code and needle set data is licensed under the [Adobe Research License](LICENSE). The license prohibits commercial use and allows non-commercial research use. For details about the haystack data, please refer to the [data/haystack/LICENSES.md](https://huggingface.co/datasets/amodaresi/NoLiMa/resolve/main/haystack/LICENSES.md) file.


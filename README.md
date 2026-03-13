# NoLiMa: Long-Context Evaluation Beyond Literal Matching

This repository contains the code and data associated with our ICML 2025 paper, "[NoLiMa: Long-Context Evaluation Beyond Literal Matching](https://arxiv.org/abs/2502.05167)".

## Abstract
> Recent large language models (LLMs) support long contexts ranging from 128K to 1M tokens. A popular method for evaluating these capabilities is the needle-in-a-haystack (NIAH) test, which involves retrieving a "needle" (relevant information) from a "haystack" (long irrelevant context). Extensions of this approach include increasing distractors, fact chaining, and in-context reasoning. However, in these benchmarks, models can exploit existing literal matches between the needle and haystack to simplify the task. To address this, we introduce **NoLiMa**, a benchmark extending NIAH with a carefully designed needle set, where questions and needles have **minimal lexical overlap, requiring models to infer latent associations to locate the needle within the haystack**. We evaluate 12 popular LLMs that claim to support contexts of at least 128K tokens. While they perform well in short contexts ($<$1K), performance degrades significantly as context length increases. At 32K, for instance, 10 models drop below 50\% of their strong short-length baselines. Even GPT-4o, one of the top-performing exceptions, experiences a reduction from an almost-perfect baseline of 99.3\% to 69.7\%. Our analysis suggests these declines stem from the increased difficulty the attention mechanism faces in longer contexts when literal matches are absent, making it harder to retrieve relevant information.

## Results
| Models               | Claimed Length | Effective Length | Base Score<br>(×0.85: Thr.) | 1K  | 2K  | 4K  | 8K  | 16K | 32K | 64K* | 128K* |
|----------------------|:-------------:|:---------------:|:-----------------------:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| GPT-4.1 🆕          | 1M            | 16K              | 97.0 (82.5)             | <ins>95.6</ins> | <ins>95.2</ins> | <ins>91.7</ins> | <ins>87.5</ins> | <ins>84.9</ins> | 79.8 | 69.7 | 64.7 |
| GPT-4o              | 128K          | 8K              | 99.3 (84.4)             | <ins>98.1</ins> | <ins>98.0</ins> | <ins>95.7</ins> | <ins>89.2</ins> | 81.6 | 69.7 | 62.4 | 56.0 |
| MiniCPM-SALA 🆕     | 1M            | 4K              | 98.2 (83.5)             | <ins>92.8</ins> | <ins>91.4</ins> | <ins>88.9</ins> | 81.5 | 71.3 | 59.7 | 53.2 | *40.9* |
| Llama 3.3 70B       | 128K          | 2K              | 97.3 (82.7)             | <ins>94.2</ins> | <ins>87.4</ins> | 81.5 | 72.1 | 59.5 | *42.7* | -- | -- |
| Llama 3.1 405B      | 128K          | 2K              | 94.7 (80.5)             | <ins>89.0</ins> | <ins>85.0</ins> | 74.5 | 60.1 | 48.4 | *38.0* | -- | -- |
| Llama 3.1 70B       | 128K          | 2K              | 94.5 (80.3)             | <ins>91.0</ins> | <ins>81.8</ins> | 71.2 | 62.7 | 51.8 | *43.2* | -- | -- |
| Gemini 1.5 Pro      | 2M            | 2K              | 92.6 (78.7)             | <ins>86.4</ins> | <ins>82.7</ins> | 75.4 | 63.9 | 55.5 | 48.2 | -- | -- |
| Jamba 1.5 Mini      | 256K          | <1K             | 92.4 (78.6)             | 76.3 | 74.1 | 70.8 | 62.2 | 52.7 | *43.6* | -- | -- |
| Command R+          | 128K          | <1K             | 90.9 (77.3)             | 77.0 | 73.5 | 66.3 | *39.5* | *21.3* | *7.4* | -- | -- |
| Llama 4 Maverick 🆕 | 1M            | 2K             | 90.1 (76.6)             | <ins>81.6</ins>  | <ins>78.3</ins> | 68.8 | 49.0 | *34.3* | *24.5* | -- | -- |
| Gemini 2.5 Flash (w/o T) 🆕 | 1M            | 2K             | 94.4 (80.2)             | <ins>90.1</ins> | <ins>86.1</ins> | 79.4 | 68.2 | 57.9 | 48.4 | -- | -- |
| Gemini 2.0 Flash 🆕 | 1M            | 4K             | 89.4 (76.0)             | <ins>87.7</ins> | <ins>87.5</ins> | <ins>77.9</ins> | 64.7 | 48.2 | *41.0* | *33.0* | *16.4* |
| Gemma 3 27B 🆕      | 128K          | <1K             | 88.6 (75.3)             | 73.3 | 65.6 | 48.1 | *32.7* | *20.2* | *9.5* | -- | -- |
| Mistral Large 2     | 128K          | 2K              | 87.9 (74.7)             | <ins>86.1</ins> | <ins>85.5</ins> | 73.3 | 51.5 | *32.6* | *18.7* | -- | -- |
| Claude 3.5 Sonnet   | 200K          | 4K              | 87.6 (74.4)             | <ins>85.4</ins> | <ins>84.0</ins> | <ins>77.6</ins> | 61.7 | 45.7 | *29.8* | -- | -- |
| Gemma 3 12B 🆕      | 128K          | 1K              | 87.4 (74.3)             | <ins>74.7</ins> | 61.8 | *39.9* | *27.4* | *16.8* | *7.3* | -- | -- |
| Gemini 1.5 Flash    | 1M            | <1K             | 84.7 (72.0)             | 68.6 | 61.6 | 51.0 | 44.4 | *35.5* | *28.6* | -- | -- |
| GPT-4o mini         | 128K          | <1K             | 84.9 (72.2)             | 67.7 | 58.2 | 44.1 | *32.6* | *20.6* | *13.7* | -- | -- |
| Llama 4 Scout 🆕    | 10M           | 1K              | 81.7 (69.4)             | <ins>72.3<ins> | 61.8 | 50.8 | *35.5* | *26.9* | *21.6* | -- | -- |
| GPT-4.1 Mini 🆕     | 1M            | <1K             | 80.9 (68.8)             | 66.7 | 62.8 | 58.7 | 51.9 | 46.2 | *38.8* | -- | -- |
| GPT-4.1 Nano 🆕     | 1M            | <1K             | 80.7 (68.6)             | 60.8 | 48.2 | *36.7* | *28.8* | *19.5* | *9.4* | -- | -- |
| Llama 3.1 8B        | 128K          | 1K              | 76.7 (65.2)             | <ins>65.7</ins> | 54.4 | 44.1 | *31.9* | *22.6* | *14.2* | -- | -- |
| Gemma 3 4B 🆕       | 128K          | <1K              | 73.6 (62.6)             | 50.3 | *35.3* | *16.4* | *7.5* | *2.3* | *0.9* | -- | -- |

This table presents the performance results of selected models on NOLIMA tests. The **base score** represents a model’s accuracy on the task at short contexts (250, 500, and 1K) and serves as a controlled reference to measure performance degradation at longer contexts. 
The **effective length** is defined as the longest context where a model maintains at least 85% of its base score. Scores above this threshold are <ins>underlined</ins>, while scores dropping below 50% of the base score are *italicized*.
Longer context evaluations (64K and 128K) use a reduced number of placements (11 instead of 26) and account for token limit constraints, particularly for GPT-4o.

#### ✨ Updates:

- [2025-07-17]: Added evaluation results on GPT-o3 and GPT-o4 Mini on NoLiMa-Hard in the reasoning models section.
- [2025-06-09]: Added support for external API providers (e.g. Fireworks, OpenRouter, ...) Added evaluation results on GPT-4.1 series, Gemini 2.5 Flash (w/o Thinking), and Llama 4 Maverick. 
Gemini 2.5 Pro and Gemini 2.5 Flash (w/ Thinking) results are included in the NoLiMa-Hard section. Added evaluation results up to 128K for GPT-4o, 4.1 and Gemini 2.0 Flash.
- [2025-04-10]: Added evaluation results on Gemma 3 models (4B/12B/27B), Gemini 2.0 Flash, and Llama 4 Scout.

### NoLiMa-Hard Results
| Models                | Base Score | 4K  | 8K  | 16K | 32K |
|-----------------------|:---------:|:---:|:---:|:---:|:---:|
| **Baselines for comparison (w/o CoT)**     |           |     |     |     |     |
| GPT-4.1              | 96.0       | 69.8 | 58.4 | 54.5 | *45.4* |
| GPT-4o               | 99.9       | 90.7 | 75.6 | 61.1 | *38.5* |
| Gemini 2.5 Flash (w/o Thinking) 🆕 | 87.5       | 47.2 | *23.5* | *13.4* | *9.8* |
| **Llama 3.3 70B**     |           |     |     |     |     |
| - w/o CoT            | 98.3       | 55.5 | *37.2* | *16.7* | *8.9* |
| - w/ CoT             | 97.1       | 73.0 | 51.2 | *31.8* | *10.1* |
| **Reasoning Models**  |           |     |     |     |     |
| GPT-o3 🆕               | 100.0      | 94.4 | 86.2 | 74.9 | 58.5 |
| MiniCPM-SALA 🆕     | 98.2       | 90.3 | 84.6 | 77.5 | 69.9 |
| Gemini 2.5 Pro 🆕    | 99.1       | 73.9 | 63.0 | 58.6 | 58.6 |
| GPT-o1               | 99.9       | 92.0 | 78.0 | 60.1 | *31.1* |
| DeepSeek R1-Distill-Llama-70B   | 99.9       | 91.4 | 75.5 | *49.4* | *20.7* |
| GPT-o3 Mini          | 98.8       | 52.8 | *36.9* | *25.5* | *18.9* |
| Gemini 2.5 Flash (w/ Thinking) 🆕  | 89.5      | 48.5 | *33.6* | *21.9* | *15.7* |
| GPT-o4 Mini 🆕          | 99.6     | 57.4 | *30.8* | *20.2* | *11.7* |


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
  - For general API providers like Fireworks or OpenRouter, you will need to specify the `tokenizer_type` and `tokenizer_model` in the model config file (e.g. check `evaluation/model_configs/llama_4_scout_EXTERNAL_API.json` for an example).
  - Some models may require additional parameters, such as `thinking_budget` for Gemini 2.5 Flash, which can be specified in the model config file.

### 4. Common Steps for Both Approaches

1. **Prepare test configuration files**  
   - Add or modify configuration files in the `evaluation/run_config` directory.  
   - Ensure they reference the correct model config file from `evaluation/model_configs`.

2. **Run the evaluations**  
   ```bash
   cd evaluation/
   ./run_tests.sh
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
If you use the **NoLiMa** dataset, filtering pipeline, or code from this repository, please cite the [paper](https://arxiv.org/abs/2502.05167):

```bibtex
@inproceedings{modarressi2025nolima,
  title={NoLiMa: Long-Context Evaluation Beyond Literal Matching},
  author={Modarressi, Ali and Deilamsalehy, Hanieh and Dernoncourt, Franck and Bui, Trung and Rossi, Ryan A. and Yoon, Seunghyun and Schütze, Hinrich},
  booktitle={Forty-second International Conference on Machine Learning},
  year={2025},
  url={https://arxiv.org/abs/2502.05167}
}
```

## License

The evaluation code and needle set data is licensed under the [Adobe Research License](LICENSE). The license prohibits commercial use and allows non-commercial research use. For details about the haystack data, please refer to the [data/haystack/LICENSES.md](https://huggingface.co/datasets/amodaresi/NoLiMa/resolve/main/haystack/LICENSES.md) file.


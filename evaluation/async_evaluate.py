# Copyright 2022 Adobe
# All Rights Reserved.

# NOTICE: Adobe permits you to use, modify, and distribute this file in
# accordance with the terms of the Adobe license agreement accompanying
# it.

import os
import json
from typing import Union
from tqdm import tqdm
import time
import asyncio
import hashlib
from copy import deepcopy

import numpy as np

from async_api_connector import APIConnector

from jsonargparse import ArgumentParser, ActionConfigFile
from data.book_haystack import BookHaystack

class NoLiMa_Tester:
    def __init__(
        self,
        model_name: str,
        model_configs_dir: str,
        needle: str,
        haystack_path: str,
        results_dir: str,
        retrieval_question: str,
        system_prompt: str,
        use_default_system_prompt: bool,
        task_template: str,
        context_length: int,
        document_depth_percent_min = 0,
        document_depth_percent_max = 100,
        document_depth_percent_intervals = 35,
        seed: int = 42,
        gold_answers: str = "",
        character_set: str = "",
        shift: int = 0,
        static_depth: float = -1,
        test_name: str = "",
        log_placements_dir: str = "",
        metric: str = "EM",
        prevent_duplicate: bool = True,
        distractor: Union[str, None] = None
    ) -> None:
        self.model_name = model_name
        self.model_config_path = os.path.join(model_configs_dir, model_name + ".json")

        if not os.path.exists(self.model_config_path):
            raise FileNotFoundError(f"Model configuration for {model_name} not found in {model_configs_dir}")

        with open(self.model_config_path, "r") as file:
            self.model_config = json.load(file)

        self.api_connector = APIConnector(
            **self.model_config
        )

        self.needle = needle
        if gold_answers != "":
            try:
                self.gold_answers = json.loads(gold_answers)
            except json.JSONDecodeError:
                self.gold_answers = gold_answers
        else:
            self.gold_answers = ""

        if character_set != "":
            try:
                self.character_set = json.loads(character_set)
            except json.JSONDecodeError:
                self.character_set = character_set
        else:
            self.character_set = ""

        self.system_prompt = system_prompt
        self.use_default_system_prompt = use_default_system_prompt
        self.task_template = task_template

        if not os.path.exists(haystack_path):
            raise FileNotFoundError(f"Haystack file not found at {haystack_path}")

        self.haystack_path = haystack_path

        self.haystack = BookHaystack(self.haystack_path)

        self.results_dir = results_dir
        os.makedirs(results_dir, exist_ok=True)

        self.retrieval_question = retrieval_question
        self.context_length = context_length
        self.document_depth_percent_min = document_depth_percent_min
        self.document_depth_percent_max = document_depth_percent_max
        self.document_depth_percent_intervals = document_depth_percent_intervals
        self.shift = shift
        self.static_depth = static_depth
        self.metric = metric
        self.seed = seed
        self.prevent_duplicate = prevent_duplicate
        self.distractor = distractor

        self.log_placements = log_placements_dir != ""
        self.log_placements_dir = log_placements_dir

        self.test_name = test_name
        self.eval_name = f"{model_name}_book_{test_name}_{int(time.time())}" if test_name != "" else f"{model_name}_book_{int(time.time())}"


    def _evaluate_response(self, response: str, gold_answers = None) -> int:
        if gold_answers is None:
            gold_answers = self.gold_answers
        if self.metric == "EM":
            return int(response.strip() in gold_answers)
        elif self.metric == "contains":
            return int(any([gold_answer in response for gold_answer in gold_answers]))
        elif self.metric == "lastline_EM":
            return int(response.strip().split("\n")[-1] in gold_answers)
        elif self.metric == "lastline_contains":
            return int(any([gold_answer in response.strip().split("\n")[-1] for gold_answer in gold_answers]))
        else:
            raise ValueError(f"Invalid metric: {self.metric}")

    def get_hash(self, test_config: dict) -> str:
        if "test_hash" in test_config:
            return test_config["test_hash"]
        new_config = deepcopy(test_config)
        del new_config["results"]
        del new_config["eval_name"]
        return hashlib.sha256(json.dumps(new_config, sort_keys=True).encode()).hexdigest()


    def evaluate(self) -> None:
        np.random.seed(self.seed)
        outputs = {
            "eval_name": self.eval_name,
            "test_name": self.test_name,
            "model_name": self.model_name,
            "model_config_path": self.model_config_path,
            "retrieval_question": self.retrieval_question,
            "needle": self.needle,
            "gold_answers": self.gold_answers,
            "system_prompt": self.api_connector.SYSTEM_PROMPT if self.use_default_system_prompt else self.system_prompt,
            "use_default_system_prompt": self.use_default_system_prompt,
            "task_template": self.task_template,
            "haystack_path": self.haystack_path,
            "haystack_hash": self.haystack.get_hash(),
            "context_length": self.context_length,
            "character_set": self.character_set,
            "document_depth_percent_min": self.document_depth_percent_min,
            "document_depth_percent_max": self.document_depth_percent_max,
            "document_depth_percent_intervals": self.document_depth_percent_intervals,
            "shift": self.shift,
            "static_depth": self.static_depth,
            "metric": self.metric,
            "result_dir": self.results_dir,
            "log_placements_dir": self.log_placements_dir,
            "seed": self.seed,
            "results": []
        }
        if self.distractor is not None:
            outputs["distractor"] = self.distractor
        outputs["test_hash"] = self.get_hash(outputs)
        results_path = os.path.join(self.results_dir, f"{self.eval_name}.json")
        if os.path.exists(results_path):
            print(f"Results already exist at {results_path}")
            print("Skipping evaluation")
            return

        if self.prevent_duplicate:
            for result_filename in os.listdir(self.results_dir):
                with open(os.path.join(self.results_dir, result_filename), "r") as file:
                    other_result = json.load(file)

                if outputs["test_hash"] == self.get_hash(other_result):
                    print(f"Duplicate test found with similar hash at {self.results_dir} -- TEST_HASH:", outputs["test_hash"])
                    print("Skipping evaluation")
                    return

        async_tasks = []
        for i in tqdm(np.linspace(self.document_depth_percent_min, self.document_depth_percent_max, self.document_depth_percent_intervals)):
            needle_depth = i / 100
            api_output = {}
            if "{CHAR}" in self.needle:
                if type(self.character_set) is not list:
                    raise ValueError("Character set not provided")
                selected_character = str(np.random.choice(self.character_set))
                api_output["selected_character"] = selected_character
                needle = self.needle.replace("{CHAR}", selected_character)
            else:
                needle = self.needle

            if "{CHAR}" in self.retrieval_question:
                retrieval_question = self.retrieval_question.replace("{CHAR}", selected_character)
            else:
                retrieval_question = self.retrieval_question

            placement_output = self.haystack.generate_w_needle_placement(
                needle=needle,
                token_count_func=self.api_connector.token_count,
                encoding_func=self.api_connector.encode,
                decoding_func=self.api_connector.decode,
                context_length=self.context_length,
                depth=needle_depth,
                shift=self.shift,
                static_depth=self.static_depth,
                distractor=self.distractor
            )

            filled_template = self.task_template.format(haystack=placement_output["text"], question=retrieval_question)

            async_tasks.append(self.api_connector.generate_response(
                system_prompt=self.system_prompt,
                user_prompt=filled_template,
                max_tokens=self.model_config["max_tokens"],
                temperature=self.model_config["temperature"],
                top_p=self.model_config["top_p"]
            ))

            api_output["placement_metadata"] = {k: v for k, v in placement_output.items() if k != "text"}

            outputs["results"].append(api_output)

            if self.log_placements:
                placement_log_path = os.path.join(self.log_placements_dir, f"{self.eval_name}_{str(np.round(i, 3))}.txt")
                with open(placement_log_path, "w") as file:
                    file.write(placement_output["text"])

        loop = asyncio.get_event_loop()

        responses = loop.run_until_complete(asyncio.gather(*async_tasks))

        for i in tqdm(range(len(responses))):
            outputs["results"][i]["metric"] = self._evaluate_response(responses[i]["response"], gold_answers=[outputs["results"][i]["selected_character"]]) if "{CHAR}" in self.needle else self._evaluate_response(responses[i]["response"])
            for k, v in responses[i].items():
                outputs["results"][i][k] = v

        # Save results by model name, haystack type, timestamp
        with open(results_path, "w") as file:
            json.dump(outputs, file, indent=4)

        print(f"Results saved at {results_path}")




if __name__ == "__main__":
    parser = ArgumentParser(description="NoLiMa Tester")
    parser.add_argument('--config', action=ActionConfigFile, help='Path to a configuration YAML file.')
    parser.add_argument("--model_name", type=str, help="Name of the model to test")
    parser.add_argument("--model_configs_dir", type=str, help="Directory containing model configurations")
    parser.add_argument("--needle", type=str, help="Needle to search in the haystack")
    parser.add_argument("--haystack_path", type=str, help="Path to the haystack file")
    parser.add_argument("--results_dir", type=str, help="Directory to save results")
    parser.add_argument("--retrieval_question", type=str, help="Question to retrieve the needle")
    parser.add_argument("--gold_answers", type=str, help="Gold answers to evaluate the response")
    parser.add_argument("--system_prompt", type=str, help="System prompt for the model")
    parser.add_argument("--use_default_system_prompt", type=bool, default=False, help="Use default system prompt")
    parser.add_argument("--task_template", type=str, help="Task template for the model")
    parser.add_argument("--context_length", type=int, help="Context length for the needle placement")
    parser.add_argument("--document_depth_percent_min", type=int, default=0, help="Minimum document depth percentage")
    parser.add_argument("--document_depth_percent_max", type=int, default=100, help="Maximum document depth percentage")
    parser.add_argument("--document_depth_percent_intervals", type=int, default=35, help="Number of intervals between min and max depth")
    parser.add_argument("--static_depth", type=float, default=-1, help="Static depth for needle placement")
    parser.add_argument("--metric", type=str, default="EM", help="Evaluation metric")
    parser.add_argument("--log_placements_dir", type=str, default="", help="Directory to save needle placements for debugging")
    parser.add_argument("--test_name", type=str, default="", help="Name of the test")
    parser.add_argument("--seed", type=int, default=42, help="Seed for random character selection")
    parser.add_argument("--distractor", type=str, default="", help="Distractor text placed in the haystack")

    args = parser.parse_args()

    tester = NoLiMa_Tester(
        model_name=args.model_name,
        model_configs_dir=args.model_configs_dir,
        needle=args.needle,
        haystack_path=args.haystack_path,
        results_dir=args.results_dir,
        retrieval_question=args.retrieval_question,
        gold_answers=args.gold_answers,
        system_prompt=args.system_prompt,
        use_default_system_prompt=args.use_default_system_prompt,
        task_template=args.task_template,
        context_length=args.context_length,
        document_depth_percent_min=args.document_depth_percent_min,
        document_depth_percent_max=args.document_depth_percent_max,
        document_depth_percent_intervals=args.document_depth_percent_intervals,
        static_depth=args.static_depth,
        metric=args.metric,
        seed=args.seed,
        distractor=args.distractor if args.distractor != "" else None,
    )

    tester.evaluate()


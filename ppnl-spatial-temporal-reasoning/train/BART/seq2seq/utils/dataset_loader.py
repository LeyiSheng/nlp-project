import json
import os
from typing import Callable, Tuple, Any
import logging
from datasets.dataset_dict import DatasetDict
from datasets.arrow_dataset import Dataset
from transformers.tokenization_utils_fast import PreTrainedTokenizerFast
from transformers.training_args import TrainingArguments
from .args import ModelArguments
from .dataset import (
	DataArguments,
	DataTrainingArguments,
	DatasetSplits,
	TrainSplit,
	_prepare_train_split,
	prepare_splits,
	)

from .spider import spider_pre_process_function

logger = logging.getLogger(__name__)


class ExactMatchMetric:
	def compute(self, predictions, references):
		labels = [reference["label"] for reference in references]
		if not labels:
			return {"exact_match": 0.0}
		count = sum(int(prediction == label) for prediction, label in zip(predictions, labels))
		return {"exact_match": count / len(labels)}


def _load_json_dataset(path: str) -> Dataset:
	with open(path, encoding="utf-8") as f:
		return Dataset.from_list(json.load(f))


def _load_ppnl_dataset_dict() -> DatasetDict:
	train_file = os.getenv("PPNL_TRAIN_FILE", "./transformers_cache/multigoal_train_updated.json")
	dev_file = os.getenv("PPNL_DEV_FILE", "./transformers_cache/multigoal_dev_updated.json")
	test_file = os.getenv("PPNL_TEST_FILE")

	splits = {
		"train": _load_json_dataset(train_file),
		"validation": _load_json_dataset(dev_file),
	}
	if test_file:
		splits["test"] = _load_json_dataset(test_file)
	return DatasetDict(splits)

def _log_duplicate_count(dataset: Dataset, dataset_name: str, split: str)-> None:
	d = dataset.to_dict()
	d_t = [tuple((k, tuple(v)) for k, v in zip(d.keys(), vs)) for vs in zip(*d.values())]
	d_t = set(d_t)
	num_examples = len(d_t)
	duplicate_count = num_examples - len(d_t)
	if duplicate_count > 0:
		logger.warning(f"The split ``{split}`` of the dataset ``{dataset_name}`` contains {duplicate_count} duplicates out of {num_examples} examples")


def load_dataset(data_args: DataArguments, model_args:ModelArguments, data_training_args: DataTrainingArguments, training_args: TrainingArguments, tokenizer: PreTrainedTokenizerFast)->Tuple[Any, DatasetSplits]:
	print('DataArgs::::{}'.format(data_args))
	_spider_dataset_dict: Callable[[], DatasetDict] = _load_ppnl_dataset_dict
	_spider_metric: Callable[[], ExactMatchMetric] = lambda: ExactMatchMetric()

	# _spider_add_serialized_schema = lambda ex: spider_add_serialized_schema(ex=ex, data_training_args=data_training_args)
	_spider_pre_process_function = lambda batch, max_source_length, max_target_length: spider_pre_process_function(batch, max_source_length, max_target_length, data_training_args, tokenizer)

	_prepare_splits_kwargs = {
	"data_args": data_args,
	"training_args": training_args,
	"data_training_args": data_training_args
	}
	if data_args.dataset == "spider":
		metric = _spider_metric()
		dataset_splits = prepare_splits(dataset_dict = _spider_dataset_dict(), pre_process_function=_spider_pre_process_function, **_prepare_splits_kwargs)
	else:
		raise NotImplementedError()
	if dataset_splits.train_split is not None:
		_log_duplicate_count(dataset=dataset_splits.train_split.dataset, dataset_name=data_args.dataset, split="train")
	if dataset_splits.eval_split is not None:
		_log_duplicate_count(dataset=dataset_splits.eval_split.dataset, dataset_name=data_args.dataset, split="eval")
	if dataset_splits.test_splits is not None:
		for section, split in dataset_splits.test_splits.items():
			_log_duplicate_count(dataset=split.dataset, dataset_name=data_args.dataset, split=section)
	return metric, dataset_splits

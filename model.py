from seq2annotation.trainer.train_model import train_model
from seq2annotation.algorithms.BiLSTM_CRF_model import BilstmCrfModel

from seq2annotation import utils
from seq2annotation.data_input.simple import input_fn as simple_input_fn
# from seq2annotation.data_input.with_lookup import input_fn as simple_input_fn
from seq2annotation.data_input.simple import generator_fn as simple_generator_fn


class Model(object):
    def __init__(self, config):
        self.config = config

    def train_and_eval_then_save(self, train_inpf, eval_inpf, configure):
        evaluate_result, export_results, final_saved_model = train_model(
            train_inpf=train_inpf,
            eval_inpf=eval_inpf,
            config=configure,
            model_fn=BilstmCrfModel.model_fn,
            model_name=BilstmCrfModel.get_model_name()
        )

        return evaluate_result, export_results, final_saved_model

    def get_default_config(self):
        data_dir = self.config.pop('data_dir', '.')
        result_dir = self.config.pop('result_dir', '.')

        params = {
            'dim': 300,
            'dropout': 0.5,
            'num_oov_buckets': 1,
            'epochs': None,
            'batch_size': 20,
            'buffer': 15000,
            'lstm_size': 100,
            'words': utils.join_path(data_dir, './unicode_char_list.txt'),
            'lookup': utils.join_path(data_dir, './lookup.txt'),
            'chars': utils.join_path(data_dir, 'vocab.chars.txt'),
            'tags': utils.join_path(data_dir, './tags.txt'),
            'glove': utils.join_path(data_dir, './glove.npz'),

            'model_dir': utils.join_path(result_dir, 'model_dir'),
            'params_log_file': utils.join_path(result_dir, 'params.json'),

            'train': utils.join_path(data_dir, '{}.conllz'.format('train')),
            'test': utils.join_path(data_dir, '{}.conllz'.format('test')),

            'preds': {
                'train': utils.join_path(result_dir, '{}.txt'.format('preds_train')),
                'test': utils.join_path(result_dir, '{}.txt'.format('preds_test')),
            },

            'optimizer_params': {},

            'saved_model_dir': utils.join_path(result_dir, 'saved_model'),

            'hook': {
                'stop_if_no_increase': {
                    'min_steps': 100,
                    'run_every_secs': 60,
                    'max_steps_without_increase': 20
                }
            },

            'train_spec': {
                'max_steps': 5000
            },
            'eval_spec': {
                'throttle_secs': 60
            },

            'estimator': {
                'save_checkpoints_secs': 120
            },


            'embedding': {
                'vocabulary_size': 128003
            },

            'use_tpu': False,
            'tpu_config': {
                'tpu_name': None,
                'zone': None,
                'gcp_project': None
            }
        }

        params.update(BilstmCrfModel.default_params())

        return params

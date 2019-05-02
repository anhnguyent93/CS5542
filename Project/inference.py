from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from os import listdir
from os.path import isfile, join
from nltk.tokenize import sent_tokenize, word_tokenize, regexp_tokenize

import logging
import math
import os

import tensorflow as tf

from module.caption_generator import CaptionGenerator
from module.model import ShowAndTellModel
from module.vocabulary import Vocabulary

from module.mt_text_score import TextScore
import module.utils as utils

FLAGS = tf.flags.FLAGS

tf.flags.DEFINE_string("model_path", "model\show-and-tell.pb", "Model graph def path")
tf.flags.DEFINE_string("vocab_file", "assets\word_counts.txt", "Text file containing the vocabulary.")
tf.flags.DEFINE_string("input_files", "dataset\\test\cat.14.jpg",
                       "File pattern or comma-separated list of file patterns "
                       "of image files.")

ref_file = "assets/test_score_ref.txt"
hyp_file = "assets/test_score_hyp.txt"
scores_file = "assets/test_score.txt"
scores_meteor_file = "assets/test_meteor.txt"

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def main(_):
    model = ShowAndTellModel(FLAGS.model_path)
    vocab = Vocabulary(FLAGS.vocab_file)
    filenames = _load_filenames()

    generator = CaptionGenerator(model, vocab)

    for filename in filenames[0:3]:
        with tf.gfile.GFile(filename, "rb") as f:
            image = f.read()

        ref = open(ref_file, "w")
        # with open("assets/captions.txt", "r") as cap_file:
        #     caps = cap_file.read().splitlines()
        #
        #     i = 0
        #     while i < len(caps):
        #         words = regexp_tokenize(caps[i], pattern='\w+\.\d+\.\w+|\w+|#\d+')
        #         if words[0] == os.path.basename(filename):
        #             ref.write(caps[i].split("\t", 1)[1])
        #             ref.write("\n")
        #
        #         i += 1
        #
        # cap_file.close()

        hyp = open(hyp_file, "w")

        captions = generator.beam_search(image)
        print("Captions for image %s:" % os.path.basename(filename))
        for i, caption in enumerate(captions):
            # Ignore begin and end tokens <S> and </S>.9
            sentence = [vocab.id_to_token(w) for w in caption.sentence[1:-1]]
            sentence = " ".join(sentence)
            print("  %d) %s (p=%f)" % (i, sentence, math.exp(caption.logprob)))
            if i == 0:
                ref.write(sentence)
                ref.write("\n")
            else:
                hyp.write(sentence)
                hyp.write("\n")

        ref.close()
        hyp.close()
        test_score_file()

def _load_filenames():
    filenames = []

    with open("F:\Courses\COMP_SCI 5542 - Big Data Analytics and Apps\Source Code\CS5542\Assignment2\etc\species_list.txt") as f:
        species = f.read().splitlines()
    for file_pattern in FLAGS.input_folder.split(","):
        for spec in species:
            for f in listdir(file_pattern + spec):
                if isfile(join(file_pattern + spec, f)):
                    filenames.extend(tf.gfile.Glob(file_pattern + spec + "\\" + f))

    logger.info("Running caption generation on %d files matching",
                len(filenames))
    return filenames

def _load_filenames():
    filenames = []
    for file_pattern in FLAGS.input_files.split(","):
        filenames.extend(tf.gfile.Glob(file_pattern))
    logger.info("Running caption generation on %d files matching %s",
                len(filenames), FLAGS.input_files)
    return filenames


def test_score_file():

    # Initialize handler for text scores
    text_score = TextScore()
    # BLEU, GLEU, WER, TER
    # text_score.score_multiple_from_file(ref_file, hyp_file, scores_file, score_type="BLEU GLEU", average_prec="corpus sent_average")
    text_score.score_multiple_from_file(ref_file, hyp_file, scores_file,
                                        score_type=utils.BLEU_NAME+utils.GOOGLE_BLEU_NAME+utils.WER_NAME+utils.TER_NAME,
                                        average_prec="corpus, sent_average")

    # METEOR: receives 2 files
    text_score.meteor_score_from_files(ref_file, hyp_file, scores_file=scores_meteor_file)


if __name__ == "__main__":
    tf.app.run()

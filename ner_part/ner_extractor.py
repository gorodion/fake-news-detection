from transformers import pipeline
from termcolor import colored
import torch


class Ner_Extractor:
    """
    source: https://huggingface.co/surdan/LaBSE_ner_nerel
    Labeling each token in sentence as named entity

    :param model_checkpoint: name or path to model
    :type model_checkpoint: string
    """

    def __init__(self, model_checkpoint: str):
        self.token_pred_pipeline = pipeline("token-classification",
                                            model=model_checkpoint,
                                            aggregation_strategy="average")

    @staticmethod
    def text_color(txt, txt_c="blue", txt_hglt="on_yellow"):
        """
        Coloring part of text

        :param txt: part of text from sentence
        :type txt: string
        :param txt_c: text color
        :type txt_c: string
        :param txt_hglt: color of text highlighting
        :type txt_hglt: string
        :return: string with color labeling
        :rtype: string
        """
        return colored(txt, txt_c, txt_hglt)

    @staticmethod
    def concat_entities(ner_result):
        """
        Concatenation entities from model output on grouped entities

        :param ner_result: output from model pipeline
        :type ner_result: list
        :return: list of grouped entities with start - end position in text
        :rtype: list
        """
        entities = []
        prev_entity = None
        prev_end = 0
        # print('---------------------------------------')
        # print('---------------------------------------')
        # print(ner_result)
        for i in range(len(ner_result)):

            if (ner_result[i]["entity_group"] == prev_entity) & \
                    (ner_result[i]["start"] == prev_end):

                entities[i - 1][2] = ner_result[i]["end"]
                prev_entity = ner_result[i]["entity_group"]
                prev_end = ner_result[i]["end"]
            else:
                entities.append([ner_result[i]["entity_group"],
                                 ner_result[i]["start"],
                                 ner_result[i]["end"]])
                prev_entity = ner_result[i]["entity_group"]
                prev_end = ner_result[i]["end"]

        return entities

    def colored_text(self, text: str, entities: list):
        """
        Highlighting in the text named entities

        :param text: sentence or a part of corpus
        :type text: string
        :param entities: concated entities on groups with start - end position in text
        :type entities: list
        :return: Highlighted sentence
        :rtype: string
        """
        colored_text = ""
        init_pos = 0
        for ent in entities:
            if ent[1] > init_pos:
                colored_text += text[init_pos: ent[1]]
                colored_text += self.text_color(text[ent[1]: ent[2]]) + f"({ent[0]})"
                init_pos = ent[2]
            else:
                colored_text += self.text_color(text[ent[1]: ent[2]]) + f"({ent[0]})"
                init_pos = ent[2]

        return colored_text

    def get_entities(self, text: str):
        """
        Extracting entities from text with them position in text

        :param text: input sentence for preparing
        :type text: string
        :return: list with entities from text
        :rtype: list
        """
        assert len(text) > 0, text
        entities = self.token_pred_pipeline(text)
        concat_ent = self.concat_entities(entities)

        return concat_ent

    def show_ents_on_text(self, text: str):
        """
        Highlighting named entities in input text

        :param text: input sentence for preparing
        :type text: string
        :return: Highlighting text
        :rtype: string
        """
        assert len(text) > 0, text
        entities = self.get_entities(text)

        return self.colored_text(text, entities)


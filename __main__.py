import logging
from tqdm import tqdm

import torch
from transformers import BatchEncoding
from torch.utils.data import DataLoader

from .dataset.dataset import QuestionDataset
from .dataset.tokenizer import QuestionTokenizer
from .const import (
    TRAIN_SET,
    TEST_SET,
    VALID_SET
)
from .network.roberta import fetch_RoBERTa_model
from .tester import Tester
from .trainer import Trainer

_LOGGER = logging.getLogger(__name__)

EPOCHS = 5000

device = torch.device(
    "cuda" if torch.cuda.is_available()
    else "mps" if torch.backends.mps.is_available()
    else "cpu"
)

if __name__ == "__main__":
    tokenizer = QuestionTokenizer()

    train_dataset = QuestionDataset(filename=TEST_SET, tokenizer=tokenizer)
    valid_dataset = QuestionDataset(filename=VALID_SET, tokenizer=tokenizer)
    test_dataset = QuestionDataset(filename=TEST_SET, tokenizer=tokenizer)

    train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
    valid_loader = DataLoader(valid_dataset, shuffle=False)
    test_loader = DataLoader(test_dataset, shuffle=False)

    num_labels = train_dataset.num_labels()
    model = fetch_RoBERTa_model(
        num_labels=num_labels
    ).to(device)

    trainer = Trainer(
        model=model,
        data_loader=train_loader,
        device=device
    )
    for epoch in tqdm(range(EPOCHS)):
        trainer.train(epoch=epoch)

    tester = Tester(
        model=model,
        data_loader=test_loader,
        device=device
    )
    tester.test()

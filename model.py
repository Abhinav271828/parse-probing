from typing import Any
from data import *

class PEGParser(pl.LightningModule):
    def __init__(self, vocab_size,
                       out_possibilities,
                       d_model=32,
                       nhead=2,
                       num_layers=3,
                       lr=0.1):
        super().__init__()
        self.lr = lr

        self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=d_model)
        layer = nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, dim_feedforward=d_model, batch_first=True)
        self.transformer = nn.TransformerEncoder(layer, num_layers=num_layers)
        self.head = nn.Linear(in_features=d_model, out_features=out_possibilities)

        self.model = nn.Sequential(
            # [bz, seq]
            self.embedding,
            # [bz, seq, d_model]
            self.transformer,
            # [bz, seq, d_model]
            self.head
            # [bz, seq, num_possibilities]
        )

    def forward(self, strings):
        return self.model(strings).flatten(0, 1)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.lr)

    def training_step(self, batch, batch_idx):
        strings, results = batch
        logits = self.forward(strings)
        loss = nn.CrossEntropyLoss()(logits, results.flatten(0, 1))
        self.log("train_loss", loss, on_step=True, on_epoch=True, prog_bar=True, logger=True)
        return loss

    def validation_step(self, batch, batch_idx):
        strings, results = batch
        logits = self.forward(strings)
        loss = nn.CrossEntropyLoss()(logits, results.flatten(0, 1))
        self.log("val_loss", loss, on_step=True, on_epoch=True, prog_bar=True, logger=True)
        return loss

    def test_step(self, batch, batch_idx):
        strings, results = batch
        bz, seq = strings.shape

        logits = self.forward(strings)
        preds = torch.argmax(logits, dim=-1)
        accuracy = (preds == results.flatten(0,1)).sum() / (bz * seq)
        return accuracy
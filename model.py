import math
from data import *

class PositionalEncoding(nn.Module):
    """
    Implements sinusoidal positional encoding.
    NB: This adds the PE vector to the embedding. It does NOT return the PE vector.
    Taken from https://pytorch.org/tutorials/beginner/transformer_tutorial.html,
    modified to be `batch_first=True`.
    """
    def __init__(self, d_model: int, dropout: float = 0.1, max_len: int = 5000):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)

        position = torch.arange(max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        pe = torch.zeros(1, max_len, d_model)
        pe[0, :, 0::2] = torch.sin(position * div_term)
        pe[0, :, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)

    def forward(self, x):
        """
        Arguments:
            x: Tensor, shape ``[batch_size, seq_len, embedding_dim]``
        """
        x = x + self.pe.repeat(x.size(0), 1, 1)
        return self.dropout(x)

class PEGParser(pl.LightningModule):
    def __init__(self, vocab_size,
                       out_possibilities,
                       d_model=32,
                       nhead=2,
                       num_layers=3,
                       max_len=20,
                       lr=0.1):
        super().__init__()
        self.lr = lr
        self.criterion = nn.CrossEntropyLoss()

        self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=d_model)
        self.pos_encoder = PositionalEncoding(d_model=d_model, max_len=max_len)
        layer = nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, dim_feedforward=d_model, batch_first=True)
        self.transformer = nn.TransformerEncoder(layer, num_layers=num_layers)
        self.head = nn.Linear(in_features=d_model, out_features=out_possibilities)

        self.model = nn.Sequential(
            # [bz, seq]
            self.embedding,
            # [bz, seq, d_model]
            self.pos_encoder,
            # [bz, seq, d_model]
            self.transformer,
            # [bz, seq, d_model]
            self.head
            # [bz, seq, out_possibilities]
        )

    def forward(self, strings):
        return self.model(strings)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.lr)

    def training_step(self, batch, batch_idx):
        strings, results = batch
        logits = self(strings)
        loss = self.criterion(logits.flatten(0, 1), results.flatten(0, 1))
        self.log("train_loss", loss, on_step=True, on_epoch=True, prog_bar=True, logger=True)
        return loss

    def validation_step(self, batch, batch_idx):
        strings, results = batch
        logits = self(strings)
        preds = torch.argmax(logits, dim=-1)
        accuracy = (preds == results).sum() / strings.numel()
        self.log("val_acc", accuracy, on_step=True, on_epoch=True, prog_bar=True, logger=True)
        return accuracy

    def test_step(self, batch, batch_idx):
        strings, results = batch
        logits = self.forward(strings)
        preds = torch.argmax(logits, dim=-1)
        accuracy = (preds == results).sum() / strings.numel()
        return accuracy
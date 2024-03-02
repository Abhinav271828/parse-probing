from model import *

VOCAB_SIZES = {
    'star': 2,
    'brack': 4,
    'expr': 15,
    'triple': 3,
    'dyck1': 2,
    'dyck3': 6
}

NUM_RESULTS = {
    'star': 2,
    'brack': 3,
    'expr': 3,
    'triple': 3,
    'dyck1': 2,
    'dyck3': 2
}

BATCH_SIZE = 1024
LR = 5e-4
LANGUAGE = 'star'

VOCAB_SIZE = VOCAB_SIZES[LANGUAGE]
OUT_POSSIBILITIES = NUM_RESULTS[LANGUAGE]

dataModule = PEGDataModule(LANGUAGE, BATCH_SIZE)
model = PEGParser(VOCAB_SIZE, OUT_POSSIBILITIES)

earlyStopper = EarlyStopping(monitor='val_loss', check_on_train_epoch_end=False)
lrFinder = LearningRateFinder()
saveCkpt = ModelCheckpoint(dirpath='models/', filename='{epoch}-{val_loss:.2f}', monitor='val_loss', save_on_train_epoch_end=False)
trainer = pl.Trainer(callbacks=[lrFinder, saveCkpt, earlyStopper], max_epochs=-1)

trainer.fit(model,
            train_dataloaders=dataModule.train_dataloader(),
            val_dataloaders=dataModule.val_dataloader())
trainer.test(model,
             dataloaders=dataModule.test_dataloader())
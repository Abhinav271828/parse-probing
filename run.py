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

SEQ_LENGTHS = {
    'star': 20,
    'brack': 20,
    'expr': 21,
    'triple': 20,
    'dyck1': 20,
    'dyck3': 20
}

BATCH_SIZE = 1024
LR = 5e-4
LANGUAGE = 'star'

VOCAB_SIZE = VOCAB_SIZES[LANGUAGE]
OUT_POSSIBILITIES = NUM_RESULTS[LANGUAGE]
MAX_LEN = SEQ_LENGTHS[LANGUAGE]

dataModule = PEGDataModule(LANGUAGE, BATCH_SIZE)
model = PEGParser(vocab_size=VOCAB_SIZE, out_possibilities=OUT_POSSIBILITIES, max_len=MAX_LEN)

earlyStopper = EarlyStopping(monitor='val_acc', mode='max', check_on_train_epoch_end=False)
lrFinder = LearningRateFinder()
saveCkpt = ModelCheckpoint(dirpath='models/', filename='{epoch}-{val_acc:.3f}', monitor='val_acc', mode='max', save_on_train_epoch_end=False)
trainer = pl.Trainer(callbacks=[lrFinder, saveCkpt, earlyStopper], max_epochs=-1)

trainer.validate(model, dataloaders=dataModule.val_dataloader())
trainer.fit(model,
            train_dataloaders=dataModule.train_dataloader(),
            val_dataloaders=dataModule.val_dataloader())
trainer.test(model,
             dataloaders=dataModule.test_dataloader())

"""
Classification Report
"""
#inputs = dataModule.test_dataset.input # [lines, L]
#outputs = dataModule.test_dataset.output # [lines, L]
#lines, L = outputs.shape
#preds = torch.zeros((lines, L))
#for i in range(0, lines, 1024):
#    if (i+1024 >= lines):
#        logits = model(inputs[i:lines, :])
#        preds[i:lines, :] = torch.argmax(logits, dim=-1)
#    else:
#        logits = model(inputs[i:i+1024, :]) # [1024, L, n]
#        preds[i:i+1024, :] = torch.argmax(logits, dim=-1)
#
#from sklearn.metrics import classification_report
#
#print((outputs == 0).sum(), (outputs == 1).sum())
#print((preds == 0).sum(), (preds == 1).sum())
#classification_report(outputs.flatten(), preds.flatten())
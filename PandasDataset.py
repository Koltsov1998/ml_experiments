from mrcnn.utils import Dataset
from os import listdir

class KangarooDataset(Dataset):
    # load the dataset definitions
    def load_dataset(self, datasetDir, is_train=True):
        self.add_class('dataset', 1, 'panda')
        imagesDir = datasetDir + '/images/'
        for fileName in listdir(imagesDir):
            imageId = fileName[:-4]
            imgPath = imagesDir
            annPath = datasetDir + imageId
            self.add_image('dataset', image_id=imageId, path=imgPath, annotation=annPath)
    # load the masks for an image
    def load_mask(self, image_id):
        # ...

    # load an image reference
    def image_reference(self, image_id):
        # ...
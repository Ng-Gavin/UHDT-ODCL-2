from dblur.testers.mscnn import MSCNNTester
from dblur.testers.stack_dmphn import StackDMPHNTester
from dblur.multi_modal_deblur import multi_modal_deblur

mscnn_tester = MSCNNTester()
model1 = mscnn_tester.get_model()

dmphn_tester = StackDMPHNTester()
model2 = dmphn_tester.get_model(num_of_stacks=1)

multi_modal_deblur(models=[model1, model2],
                   model_names=["NAFNet"],
                   model_paths=['/Users/paul/Documents/School/UHDT/Training Data/NAFNet-GoPro-width32.pth'],
                   blur_img_path=blur_img_path,
                   sharp_img_path=sharp_img_path,
                   is_checkpoint=[True, True],
                   window_slicing=True,
                   window_size=256,
                   overlap_size=0)
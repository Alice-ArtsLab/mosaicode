def adjust_images_size():
    return r"""
// And, Xor, Division, subtraction, sum and multiplication need images with the same size
void adjust_images_size(IplImage * img1, IplImage * img2, IplImage * img3){
    if(img1->width != img2->width || img1->height != img2->height){
	int minW,minH;
	if(img1->width > img2->width)
		minW = img2->width;
	else 
		minW = img1->width;

	if(img1->height > img2->height)
		minH = img2->height;
	else 
		minH = img1->height;

	cvSetImageROI(img2, cvRect( 0, 0, minW, minH ));
	cvSetImageROI(img1, cvRect( 0, 0, minW, minH ));
	cvSetImageROI(img3, cvRect( 0, 0, minW, minH ));
    }
}
"""


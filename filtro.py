'''
img=imread('image.jpg')  // lê a imagem \n
img2=cvtColor(img,COLOR_BGR2GRAY)  //  preto e branco \n
img3=bitwise_not(img2)  //  preto e branco invertida \n
img4=GaussianBlur(img3,(27,27),0)  //  blur \n
img5=bitwise_not(img4)  //  blur invertida \n
img6=divide(img2,img5,scale=256.0)  //  desenho \n
'''
import cv2

COLOR_BGR2GRAY = cv2.COLOR_BGR2GRAY
imread = cv2.imread
cvtColor = cv2.cvtColor
GaussianBlur = cv2.GaussianBlur
divide = cv2.divide
imshow = cv2.imshow
waitKey = cv2.waitKey
imwrite = cv2.imwrite
destroyAllWindows = cv2.destroyAllWindows

def filtro(arquivo:str,filtro:int):
    img = imread(arquivo)
    img2 = cvtColor(img,cv2.COLOR_BGR2GRAY)
    img3 = GaussianBlur(img2,(filtro,filtro),0)
    img4 = divide(img2,img3,scale=256.0)
    imshow("imagem convertida",img4)

    split : str = arquivo.split('.')
    arquivo = arquivo.replace('.jpg','_novo.jpg') if split[len(split)-1] == 'jpg'\
    else f'{ arquivo.removesuffix(".png") }_novo.png'
    
    waitKey(0)
    imwrite(arquivo,img4)
    destroyAllWindows()

if __name__ == '__main__': filtro('python.jpg',101)
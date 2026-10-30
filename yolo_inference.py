from ultralytics import YOLO
import argparse

def main():
    parser = argparse.ArgumentParser("YOLO26 detection")
    parser.add_argument('--model', default='runs/detect/train-3/weights/best.pt')
    parser.add_argument('--source', default='input_videos/08fd33_4.mp4')
    args = parser.parse_args()

    model = YOLO(args.model)

    for result in model.predict(source=args.source, show=True, stream=True, save=True, save_dir='output'):
        pass

if __name__ == '__main__':
    main()


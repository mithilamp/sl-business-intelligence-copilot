from pathlib import Path
import fitz  # pymupdf


class LandDocumentParser:

    def parse(self, file_path: str):

        extension = Path(file_path).suffix.lower()

        if extension == ".pdf":
            return self._parse_pdf(file_path)

        elif extension in [".jpg", ".jpeg", ".png"]:
            return [
                file_path
            ]

        else:
            raise ValueError(
                "Unsupported file type"
            )


    def _parse_pdf(
        self,
        file_path: str
    ):

        document = fitz.open(file_path)

        images = []

        BASE_DIR = Path(__file__).resolve().parents[3]

        output_dir = (
            BASE_DIR /
            "data" /
            "rendered_land"
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_dir.mkdir(
            exist_ok=True
        )


        for index, page in enumerate(document):

            pix = page.get_pixmap(
                dpi=200
            )

            image_path = (
                output_dir /
                f"page_{index}.png"
            )

            pix.save(
                str(image_path)
            )

            images.append(
                str(image_path)
            )


        return images
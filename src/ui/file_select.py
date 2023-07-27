import os
import fitz
 
from supervisely.app.widgets import (
    Button,
    Card,
    Field,
    Container,
    Text,
    FileStorageUpload,
    SlyTqdm
)

import shutil
import supervisely as sly

from supervisely.app.widgets import (
    Button,
    Card,
    Container,
    Input,
    ProjectThumbnail,
    SelectWorkspace,
    SlyTqdm,
    Text,
    Checkbox
)

import src.globals as g


def process():
    """
    Create Project and import data
    """
    def convert_upload(file,pdf_path,dataset):
        output_text.set(text=f"Uploading {file}", status="text")
        output_text.show()
        output_progress2.show()
        pdf_document = fitz.open(pdf_path)
        with output_progress2(total=pdf_document.page_count) as pbar2:
            for page_number in range(pdf_document.page_count):
                page = pdf_document.load_page(page_number)
                # image_matrix = fitz.Matrix(fitz.Identity)
                # image_matrix.preScale(2, 2)  # Adjust scale as needed
                # Get the image in Pixmap format (which can be saved as an image file)
                pixmap = page.get_pixmap(dpi=300)
                # Save the image to a file
                image_name = file[:-4]+'_page_' + str(page_number) + '.png'
                image_path = os.path.join('output_sly', image_name)
                pixmap.save(image_path)
                try:
                    info = g.api.image.upload_path(dataset_id=dataset.id, name=image_name,
                                                path=image_path)
                    sly.logger.trace(f"Image has been uploaded: id={info.id}, name={info.name}")
                except Exception as e:
                    sly.logger.warn("Skip image", extra={"name": file, "reason": repr(e)})
                finally:
                    # Update progress bar
                    pbar2.update(1)
            pbar2.reset()
        return pdf_document.close()

    ws_selector = SelectWorkspace(default_id=g.WORKSPACE_ID, team_id=g.TEAM_ID)
    output_project_name = Input(value="My Project")
    start_import_btn = Button(text="Start Import")
    output_project_thumbnail = ProjectThumbnail()
    output_project_thumbnail.hide()
    output_text = Text()
    output_text.hide()
    output_progress = SlyTqdm(show_percents=True,message='Uploading')
    output_progress2 = SlyTqdm(show_percents=True,message='Uploading')
    output_progress.hide()
    output_progress2.hide()
    remove_source_files = Checkbox("Remove source files after successful import", checked=True)
    output_container = Container(
        widgets=[ws_selector, output_project_name, output_project_thumbnail, output_text, output_progress,
                output_progress2, start_import_btn, remove_source_files]
    )
    file_upload = FileStorageUpload(
                                    team_id=g.TEAM_ID,
                                    path="input",
                                )

    upload_1 = Field(
                    title="Upload folder with PDF files",
                    description="Make sure that you are uploading folder",
                    content=file_upload,                   
                )
    
    upload_container = Container([upload_1])

    card = Card(
                title="File Storage Upload",
                content=Container([upload_container,output_container]),
            )

    @start_import_btn.click
    def take_root():
        try:
            paths = file_upload.get_uploaded_paths()
            common_path = os.path.commonpath(paths)
            g.api.file.download_directory(g.TEAM_ID, common_path, 'input')
            os.mkdir('output_sly')
        except Exception as e:
            output_text.set(text="Something wrong with file uploading", status="error")
            output_text.show()
        output_text.set(text="Uploading", status="text")
        output_text.show()
        output_progress.show()

        # Create project and dataset on Supervisely server
        project = g.api.project.create(g.WORKSPACE_ID, output_project_name.get_value() , change_name_if_conflict=True)
        dataset_ground = g.api.dataset.create(project.id, 'ds0', change_name_if_conflict=True)
        with output_progress(total=len(paths)) as pbar:
            try:
                objects = os.listdir('input')
                for object in objects:
                    if os.path.isdir(os.path.join('input',object)):
                        path_folder = os.path.join('input',object)
                        dataset_folder = g.api.dataset.create(project.id, object, change_name_if_conflict=True)
                        for rootdir, dirs, files in os.walk(path_folder):
                            for file in files:
                                if file.endswith('pdf'):
                                    convert_upload(file,pdf_path=os.path.join(rootdir,file),dataset=dataset_folder)
                                    pbar.update(1)
                    elif object.endswith('pdf'):
                        convert_upload(object,pdf_path=os.path.join('input',object),dataset=dataset_ground)
                        pbar.update(1)
                output_progress2.hide()
                output_text.set('Success!',status='success')
                output_text.show()
            except Exception as e:
                output_text.set(text='Oops! Something wrong!', status='error')
                output_text.show()
                shutil.rmtree('input')
                shutil.rmtree('output_sly')
            finally:
                if remove_source_files and os.path.isdir('output_sly'):
                    shutil.rmtree("output_sly")
                    shutil.rmtree("input")
                    return
    return card

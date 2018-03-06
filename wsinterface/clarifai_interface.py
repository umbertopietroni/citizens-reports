# clarifai interface
import tempfile

from clarifai.rest import ClarifaiApp

def clarifai_prediction(si, apikey):
	app = ClarifaiApp(api_key=apikey)
	model = app.models.get("general-v1.3")
	img_content = si.getContent()
	fp = tempfile.NamedTemporaryFile()
	fp.write(img_content)
	fname = fp.name
	dic = model.predict_by_filename(fname)
	fp.close()
	return dic



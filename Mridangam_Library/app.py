import streamlit as st
from pathlib import Path 
from supabase_config import supabase
import uuid

st.set_page_config(
	page_title="Mridangam Library",
	page_icon="🥁",
	layout="wide")

st.title("Mridangam Library")


page=st.sidebar.radio("Choose Section: ",["Home","Notes","Audio","Video","Community Uploads"])

notes_dir=Path("data/notes")
audio_dir=Path("data/audio")
video_dir=Path("data/videos")

if page == "Home": 
	st.text("""Bridging the timeless tradition of Carnatic rhythm with modern digital learning. 
Access notes, audio tracks, and video guides in one unified space.""")

	st.subheader("About the Mridangam:")
	st.text("""The mridangam is the premier percussion instrument of South Indian Carnatic music, revered as a Deva Vadyam (divine instrument) with a history spanning thousands of years. Its name is derived from the Sanskrit words mrit (clay) and ang (body), reflecting its ancient roots when the instrument's hollow barrel was crafted from baked earth, though modern mridangams are meticulously carved from a single block of jackwood. It features a dual-headed design layered with multiple skins, including a permanent black paste center on the right head that gives the instrument its signature metallic timbre and precise tonal tuning. As the heartbeat of a Carnatic ensemble, the mridangam is not merely an accompaniment; it holds the vital responsibility of keeping the thalam (rhythmic cycle), driving the pace, and engaging in complex, mathematical rhythmic dialogues (sollukattus) that elevate the spiritual and artistic essence of the music.""")

	st.image("assets/mridangam_wallpaper_4k.jpg")
	st.markdown("<span style='color:red;font-family:Times New Roman'>Fun Fact: The four building blocks of mridangam are the words, Tha Dhi Thom Nam, which make up nearly every lesson learned in mridangam classes.</span>", unsafe_allow_html=True)

	st.subheader("About the founder:")
	st.text("""The Mridangam Library was envisioned and built by Pranav Balakrishnan, a passionate student of music and mathematics who recognized a modern challenge in traditional learning. Recognizing how easily valuable hand-written notations, audio snippets, and practice videos can get scattered across notebook pages and chat threads, Pranav combined his technical skills with his deep appreciation for rhythmic artistry to build this centralized digital space. Guided by a love for Indian classical percussion and an eye for structured, analytical thinking, he engineered this platform to ensure that the rich heritage of the mridangam is preserved, organized, and easily accessible for a new generation of digital learners.""")

elif page == "Notes":
	st.subheader("Notes")
	pdfs=list(notes_dir.glob("*.pdf"))
	
	if not pdfs:
		st.info("No PDFs found.")
	else:
		selected_notes=st.selectbox("Choose a PDF",[pdf.name for pdf in pdfs])
		pdfpath=notes_dir/selected_notes

		with open(pdfpath,"rb") as f:
			pdf1=f.read()
			st.pdf(pdf1)
			st.download_button(
				label=f"Download {pdfpath.name}",
				data=pdf1,
				file_name=pdfpath.name)

elif page == "Audio":
	st.subheader("Audio Recordings")
	audios=list(audio_dir.glob("*"))

	if not audios:
		st.info("No audio recordings found.")
	else:
		selected_audio=st.selectbox("Choose an Audio file",[audio.name for audio in audios])
		audio_path=audio_dir/selected_audio

		st.write(audio_path.stem)
		st.audio(str(audio_path))

elif page == "Video":
	st.subheader("Video Recordings")
	videos=list(video_dir.glob("*"))

	if not videos:
		st.info("No video recordings found.")
	else:
		selected_video=st.selectbox("Choose a video",[video.name for video in videos])
		video_path=video_dir/selected_video

		st.write(video_path.stem)
		st.video(str(video_path))

elif page == "Community Uploads":
	st.subheader("Community Uploads")
	title=st.text_input("Title")
	uploader=st.text_input("Your name: ")
	category=st.selectbox("Category: ",["Notes","Audio","Video"])

	uploaded_file=st.file_uploader("Choose File")

	if st.button("Upload"):
		if title == "":
			st.error("Please enter a title.")
		elif uploader == "":
			st.error("Please enter your name: ")
		elif uploaded_file is None:
			st.error("Please select a file.")	
		else:
			unique_name=f"{uuid.uuid4()}_{uploaded_file.name}"
			path = (f"{category}/{unique_name}")

			file_bytes=uploaded_file.read()
			supabase.storage.from_(
			"community-files"
			).upload(
			path,
			file_bytes,
			{
			"content-type":uploaded_file.type
			}
			)

			file_url=(supabase.storage.from_("community-files").get_public_url(path))

			supabase.table(
			    "uploads"
			).insert(
			{
			    "title": title,
			    "uploader": uploader,
			    "category": category,
			    "file_url": file_url,
			    "storage_path":path
			}
			).execute()
			st.success("Uploaded successfully!!")

	uploads=(supabase.table("uploads").select("*").execute())
	for item in uploads.data:
		st.write(item["title"])
		st.write(item["uploader"])
		st.link_button("Open",item["file_url"])

		if st.button(f"Delete {item['id']}"):
			supabase.storage.from_("community-files").remove([item["storage_path"]])
			supabase.table("uploads").delete().eq("id",item["id"]).execute()
			st.success("DELETED!")
			st.rerun()
		st.divider()
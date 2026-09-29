import os
import streamlit as st
from pytubefix import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip

st.set_page_config(page_title="AI Shorts Generator", page_icon="🎬", layout="centered")

st.title("🎬 AI Video to Shorts Clipper")
st.write("ইউটিউব লিংক দিন এবং আপনার ভিডিও থেকে ক্লিপ আলাদা করুন।")

youtube_url = st.text_input("ইউটিউব ভিডিওর লিংক দিন (YouTube URL):")

if st.button("ক্লিপ তৈরি করুন (Generate Shorts)"):
    if not youtube_url:
        st.warning("দয়া করে সঠিক ইউটিউব লিংক দিন!")
    else:
        with st.spinner("ভিডিও প্রসেস করা হচ্ছে, দয়া করে অপেক্ষা করুন..."):
            try:
                yt = YouTube(youtube_url)
                st.write(f"**ভিডিওর নাম:** {yt.title}")
                
                # আপডেট করা ডাউনলোড পদ্ধতি (সবচেয়ে ভালো উপলব্ধ স্ট্রিম ফিল্টার করা)
                stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                
                if not stream:
                    # যদি প্রগ্রেসিভ না পাওয়া যায়, তবে যেকোনো একটি স্ট্রিম নেওয়ার চেষ্টা করবে
                    stream = yt.streams.get_lowest_resolution()
                
                downloaded_file = stream.download(filename="input_video.mp4")
                
                clip = VideoFileClip(downloaded_file)
                duration = clip.duration
                
                st.success("ভিডিও সফলভাবে ডাউনলোড হয়েছে!")
                st.info(f"মোট ভিডিওর দৈর্ঘ্য: {int(duration)} সেকেন্ড")
                
                end_time = min(30, duration)
                short_clip = clip.subclipped(0, end_time)
                
                output_filename = "output_short.mp4"
                short_clip.write_videofile(output_filename, codec="libx264", audio_codec="aac")
                
                clip.close()
                short_clip.close()
                
                st.success("আপনার শর্টস ক্লিপ তৈরি হয়ে গেছে!")
                
                with open(output_filename, "rb") as file:
                    st.download_button(
                        label="ডাউনলোড শর্টস (Download Short)",
                        data=file,
                        file_name="viral_short.mp4",
                        mime="video/mp4"
                    )
                    
            except Exception as e:
                st.error(f"একটি সমস্যা হয়েছে: {e}")

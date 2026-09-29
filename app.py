import os
import streamlit as st
import yt_dlp
from moviepy.video.io.VideoFileClip import VideoFileClip

st.set_page_config(page_title="AI Shorts Generator", page_icon="🎬", layout="centered")

st.title("🎬 AI Video to Shorts Clipper")
st.write("ইউটিউব লিংক দিন এবং আপনার ভিডিও থেকে ক্লিপ আলাদা করুন।")

youtube_url = st.text_input("ইউটিউব ভিডিওর লিংক দিন (YouTube URL):")

if st.button("ক্লিপ তৈরি করুন (Generate Shorts)"):
    if not youtube_url:
        st.warning("দয়া করে সঠিক ইউটিউব লিংক দিন!")
    else:
        with st.spinner("ভিডিও ডাউনলোড এবং প্রসেস করা হচ্ছে, দয়া করে অপেক্ষা করুন... কাজ চলতে থাকুক..."):
            try:
                # yt-dlp দিয়ে ভিডিও ডাউনলোডের কনফিগারেশন
                output_template = "input_video.mp4"
                ydl_opts = {
                    'format': 'best[ext=mp4]/best',
                    'outtmpl': output_template,
                    'noplaylist': True,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(youtube_url, download=True)
                    video_title = info_dict.get('title', 'Unknown Video')
                
                st.write(f"**ভিডিওর নাম:** {video_title}")
                st.success("ভিডিও সফলভাবে ডাউনলোড হয়েছে!")
                
                # Moviepy দিয়ে ভিডিও প্রসেস করা
                clip = VideoFileClip(output_template)
                duration = clip.duration
                st.info(f"মোট ভিডিওর দৈর্ঘ্য: {int(duration)} সেকেন্ড")
                
                # প্রথম ৩০ সেকেন্ডের ক্লিপ কেটে নেওয়া (এআই বা কাস্টম সময় অনুযায়ী)
                end_time = min(30, duration)
                short_clip = clip.subclipped(0, end_time)
                
                output_filename = "output_short.mp4"
                short_clip.write_videofile(output_filename, codec="libx264", audio_codec="aac")
                
                clip.close()
                short_clip.close()
                
                st.success("আপনার শর্টস ক্লিপ তৈরি হয়ে গেছে!")
                
                # ডাউনলোড বাটন
                with open(output_filename, "rb") as file:
                    st.download_button(
                        label="ডাউনলোড শর্টস (Download Short)",
                        data=file,
                        file_name="viral_short.mp4",
                        mime="video/mp4"
                    )
                    
            except Exception as e:
                st.error(f"একটি সমস্যা হয়েছে: {e}")

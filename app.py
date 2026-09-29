import os
import streamlit as st
from pytubefix import YouTube  # ইউটিউব ভিডিও ডাউনলোড করার জন্য
from moviepy.video.io.VideoFileClip import VideoFileClip  # ভিডিও কাটার জন্য

# পেজের ডিজাইন ও টাইটেল
st.set_page_config(page_title="AI Shorts Generator", page_icon="🎬", layout="centered")

st.title("🎬 AI Video to Shorts Clipper")
st.write("ইউটিউব লিংক দিন এবং আপনার ভিডিও থেকে ক্লিপ আলাদা করুন।")

# ইনপুট নেওয়ার ঘর
youtube_url = st.text_input("ইউটিউব ভিডিওর লিংক দিন (YouTube URL):")

if st.button("ক্লিপ তৈরি করুন (Generate Shorts)"):
    if not youtube_url:
        st.warning("দয়া করে একটি সঠিক ইউটিউব লিংক দিন!")
    else:
        with st.spinner("ভিডিও প্রসেস করা হচ্ছে, দয়া করে অপেক্ষা করুন..."):
            try:
                # ১. ইউটিউব ভিডিও ডাউনলোড করা
                yt = YouTube(youtube_url)
                st.write(f"**ভিডিওর নাম:** {yt.title}")
                
                # সবচেয়ে ভালো রেজুলেশনের স্ট্রিম নির্বাচন
                stream = yt.streams.get_highest_resolution()
                downloaded_file = stream.download(filename="input_video.mp4")
                
                # ২. ভিডিও লোড করা (Moviepy দিয়ে)
                clip = VideoFileClip(downloaded_file)
                duration = clip.duration
                
                st.success("ভিডিও সফলভাবে ডাউনলোড হয়েছে!")
                st.info(f"মোট ভিডিওর দৈর্ঘ্য: {int(duration)} সেকেন্ড")
                
                # উদাহরণস্বরূপ: প্রথম ১ মিনিটের ভিডিও থেকে প্রথম ৩০ সেকেন্ডের একটি শর্টস ক্লিপ কেটে নেওয়া
                # (এআই মডেল যুক্ত করলে এটি অটোমেটিক ভাইরাল অংশ সিলেক্ট করবে)
                end_time = min(30, duration)
                short_clip = clip.subclipped(0, end_time)
                
                output_filename = "output_short.mp4"
                short_clip.write_videofile(output_filename, codec="libx264", audio_codec="aac")
                
                # ফাইল রিলিজ করা
                clip.close()
                short_clip.close()
                
                st.success("আপনার শর্টস ক্লিপ তৈরি হয়ে গেছে!")
                
                # ৩. ডাউনলোড বাটন দেখানো
                with open(output_filename, "rb") as file:
                    st.download_button(
                        label="ডাউনলোড শর্টস (Download Short)",
                        data=file,
                        file_name="viral_short.mp4",
                        mime="video/mp4"
                    )
                    
            except Exception as e:
                st.error(f"একটি সমস্যা হয়েছে: {e}")
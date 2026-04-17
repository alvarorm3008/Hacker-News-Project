import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Profile from './components/Profile';
import News from './components/News';
import SubmissionDetail from './components/submissions/SubmissionDetail';
import Submit from './components/submissions/Submit';
import Ask from './components/Ask';
import EditSubmission from './components/submissions/EditSubmission';
import Newest from './components/Newest';
import Threads from './components/Threads';
import UserProfile from './components/UserProfile';
import HiddenSubmissions from './components/HiddenSubmissions';
import UserSubmissions from './components/submissions/UserSubmissions';
import VotedSubmissions from './components/submissions/VotedSubmissions';
import FavoriteComments from './components/FavoriteComments'; 
import FavoriteSubmission from './components/submissions/FavoriteSubmission';
import Comments from './components/comments/Comments';
import DeleteComment from './components/comments/DeleteComment';
import CommentDetail from './components/comments/CommentDetail';
import UserComments from './components/comments/UserComments';
import EditComment from './components/comments/EditComment';
import VotedComments from './components/comments/VotedComments';
import ReplyComment from './components/comments/ReplyComment';
import Search from './components/Search';



const App = () => {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<News />} />
        <Route path="/submission/:id" element={<SubmissionDetail />} />
        <Route path="/submission" element={<Submit />} />
        <Route path="/ask" element={<Ask />} />
        <Route path="/newest" element={<Newest />} />
        <Route path="/threads" element={<Threads />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/author/:username/profile" element={<UserProfile />} />
        <Route path="/submissionedit/:id" element={<EditSubmission />} />
        <Route path="/hidden" element={<HiddenSubmissions />} />
        <Route path="/submissions/:username" element={<UserSubmissions />} />
        <Route path="/voted" element={<VotedSubmissions />} />
        <Route path="/favorites/:username" element={<FavoriteSubmission />} />
        <Route path="/favorite-comments/:username" element={<FavoriteComments />} />
        <Route path="/comments" element={<Comments />} />
        <Route path="/comments/:id/delete" element={<DeleteComment />} />
        <Route path="/comment/:id" element={<CommentDetail />} />
        <Route path="/comments/:username" element={<UserComments />} />
        <Route path="/comments/:id/edit" element={<EditComment />} />
        <Route path="/voted-comments" element={<VotedComments />} />
        <Route path="/comments/:id/reply" element={<ReplyComment />} />
        <Route path="/search" element={<Search />} />

        </Routes>
    </Router>
  );
};

export default App;

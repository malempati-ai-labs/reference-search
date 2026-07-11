import { Route, Routes } from 'react-router-dom';

import { Layout } from './components/layout';
import { AddCaseStudyPage } from './pages/add-case-study-page';
import { SearchPage } from './pages/search-page';

const App = () => {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<SearchPage />} />
        <Route path="add-case-study" element={<AddCaseStudyPage />} />
      </Route>
    </Routes>
  );
};

export { App };

import { useMutation } from '@tanstack/react-query';

import { createCaseStudies } from '../../../lib/api/case-studies';

export const useCreateCaseStudies = () =>
  useMutation({ mutationFn: createCaseStudies });

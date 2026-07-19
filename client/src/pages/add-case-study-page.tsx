import { Building2, Info, Plus, Trash2 } from 'lucide-react';
import {
  useFieldArray,
  useForm,
  type Control,
  type FieldErrors,
  type UseFormRegister,
} from 'react-hook-form';

interface CaseStudyFormValues {
  companies: {
    companyName: string;
    challenges: { value: string }[];
    outcomes: { value: string }[];
  }[];
}

interface CreateCaseStudiesPayload {
  caseStudies: {
    companyName: string;
    challenges: string[];
    outcomes: string[];
  }[];
}

const REQUIRED_MESSAGE = 'Required';

const createEmptyCompany = () => ({
  companyName: '',
  challenges: [{ value: '' }],
  outcomes: [{ value: '' }],
});

const notBlank = (value: string) => value.trim().length > 0 || REQUIRED_MESSAGE;

interface DynamicFieldListProps {
  control: Control<CaseStudyFormValues>;
  register: UseFormRegister<CaseStudyFormValues>;
  errors: FieldErrors<CaseStudyFormValues>;
  companyIndex: number;
  name: 'challenges' | 'outcomes';
  label: string;
  addLabel: string;
  placeholder: string;
}

const DynamicFieldList = ({
  control,
  register,
  errors,
  companyIndex,
  name,
  label,
  addLabel,
  placeholder,
}: DynamicFieldListProps) => {
  const { fields, append, remove } = useFieldArray({
    control,
    name: `companies.${companyIndex}.${name}`,
  });

  return (
    <div>
      <label className="block text-sm font-medium text-slate-900">{label}</label>
      {fields.map((field, itemIndex) => {
        const itemError = errors.companies?.[companyIndex]?.[name]?.[itemIndex]?.value;

        return (
          <div key={field.id} className="mt-2">
            <div
              className={`flex items-center gap-2 rounded-xl border px-4 py-3 ${
                itemError ? 'border-red-300' : 'border-slate-200'
              }`}
            >
              <input
                type="text"
                placeholder={placeholder}
                className="min-w-0 flex-1 border-none bg-transparent text-slate-700 placeholder:text-slate-400 focus:outline-none"
                {...register(`companies.${companyIndex}.${name}.${itemIndex}.value`, {
                  validate: notBlank,
                })}
              />
              <button
                type="button"
                onClick={() => remove(itemIndex)}
                disabled={fields.length === 1}
                aria-label={`Remove ${label.toLowerCase()} ${itemIndex + 1}`}
                className="shrink-0 text-slate-400 transition-colors hover:text-slate-600 disabled:cursor-not-allowed disabled:opacity-30 disabled:hover:text-slate-400"
              >
                <Trash2 className="h-4 w-4" />
              </button>
            </div>
            {itemError && <p className="mt-1 text-xs text-red-500">{itemError.message}</p>}
          </div>
        );
      })}
      <button
        type="button"
        onClick={() => append({ value: '' })}
        className="mt-3 flex items-center gap-1.5 text-sm font-medium text-blue-600 hover:text-blue-700"
      >
        <Plus className="h-4 w-4" />
        {addLabel}
      </button>
    </div>
  );
};

interface CompanySectionProps {
  control: Control<CaseStudyFormValues>;
  register: UseFormRegister<CaseStudyFormValues>;
  errors: FieldErrors<CaseStudyFormValues>;
  companyIndex: number;
  canRemove: boolean;
  onRemove: () => void;
}

const CompanySection = ({
  control,
  register,
  errors,
  companyIndex,
  canRemove,
  onRemove,
}: CompanySectionProps) => {
  const companyNameError = errors.companies?.[companyIndex]?.companyName;

  return (
    <div className="mt-8 rounded-2xl border border-slate-200 bg-white p-6">
      <div className="flex items-center justify-between">
        <p className="text-sm font-medium text-slate-500">Company {companyIndex + 1}</p>
        {canRemove && (
          <button
            type="button"
            onClick={onRemove}
            aria-label={`Remove company ${companyIndex + 1}`}
            className="text-slate-400 transition-colors hover:text-slate-600"
          >
            <Trash2 className="h-4 w-4" />
          </button>
        )}
      </div>

      <label className="mt-4 block text-sm font-medium text-slate-900">Company name</label>
      <div
        className={`mt-2 flex items-center gap-2 rounded-xl border px-4 py-3 ${
          companyNameError ? 'border-red-300' : 'border-slate-200'
        }`}
      >
        <Building2 className="h-4 w-4 shrink-0 text-slate-400" />
        <input
          type="text"
          placeholder="e.g. SHOPcloud360"
          className="min-w-0 flex-1 border-none bg-transparent text-slate-700 placeholder:text-slate-400 focus:outline-none"
          {...register(`companies.${companyIndex}.companyName`, { validate: notBlank })}
        />
      </div>
      {companyNameError && (
        <p className="mt-1 text-xs text-red-500">{companyNameError.message}</p>
      )}

      <div className="mt-6 grid grid-cols-1 gap-6 sm:grid-cols-2">
        <DynamicFieldList
          control={control}
          register={register}
          errors={errors}
          companyIndex={companyIndex}
          name="challenges"
          label="Challenges"
          addLabel="Add challenge"
          placeholder="e.g. Managing a catalog of one million"
        />
        <DynamicFieldList
          control={control}
          register={register}
          errors={errors}
          companyIndex={companyIndex}
          name="outcomes"
          label="Outcomes"
          addLabel="Add outcome"
          placeholder="e.g. 350 online shops managed central"
        />
      </div>
    </div>
  );
};

export const AddCaseStudyPage = () => {
  const {
    control,
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<CaseStudyFormValues>({
    defaultValues: { companies: [createEmptyCompany()] },
  });

  const {
    fields: companyFields,
    append: appendCompany,
    remove: removeCompany,
  } = useFieldArray({ control, name: 'companies' });

  const onSubmit = (values: CaseStudyFormValues) => {
    const payload: CreateCaseStudiesPayload = {
      caseStudies: values.companies.map((company) => ({
        companyName: company.companyName.trim(),
        challenges: company.challenges.map((challenge) => challenge.value.trim()),
        outcomes: company.outcomes.map((outcome) => outcome.value.trim()),
      })),
    };
    console.log(payload);
  };

  return (
    <form className="mx-auto max-w-3xl px-6 py-16" onSubmit={handleSubmit(onSubmit)}>
      <h1 className="text-4xl font-bold text-slate-900">Add case studies</h1>
      <p className="mt-4 text-lg text-slate-500">
        Grow the reference library. Add one or more companies with their challenges and outcomes
        — they'll be embedded and made searchable.
      </p>

      <div className="mt-8 flex items-start gap-3 rounded-xl border border-blue-100 bg-blue-50 px-5 py-4 text-sm text-blue-700">
        <Info className="mt-0.5 h-5 w-5 shrink-0" />
        <p>
          Submitting rebuilds the entire vector index server-side. This can take a while as the
          library grows — the form stays disabled until it's done. Duplicate company names are
          skipped automatically.
        </p>
      </div>

      {companyFields.map((companyField, companyIndex) => (
        <CompanySection
          key={companyField.id}
          control={control}
          register={register}
          errors={errors}
          companyIndex={companyIndex}
          canRemove={companyIndex > 0}
          onRemove={() => removeCompany(companyIndex)}
        />
      ))}

      <button
        type="button"
        onClick={() => appendCompany(createEmptyCompany())}
        className="mt-6 flex w-full items-center justify-center gap-2 rounded-2xl border border-dashed border-slate-300 bg-white py-4 text-sm font-medium text-slate-500 transition-colors hover:border-slate-400"
      >
        <Plus className="h-4 w-4" />
        Add another company
      </button>

      <div className="mt-8 flex justify-end">
        <button
          type="submit"
          className="flex items-center gap-2 rounded-full bg-blue-500 px-6 py-3 text-sm font-medium text-white transition-colors hover:bg-blue-600"
        >
          <Plus className="h-4 w-4" />
          Add to knowledge base
        </button>
      </div>
    </form>
  );
};

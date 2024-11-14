import PropTypes from 'prop-types' // Import PropTypes for prop validation

function Headline({ data }) {
  return (
    <div className="headline flex justify-center items-center py-2">
      <a
        href={data.link}
        target="_blank"
        rel="noreferrer"
        className="text-gray-800 hover:text-blue-600 font-medium text-lg md:text-base transition-transform transform hover:scale-105 duration-200 block truncate "
      >
        {data.headline}
      </a>
    </div>
  )
}

// Define propTypes for the component
Headline.propTypes = {
  data: PropTypes.shape({
    headline: PropTypes.string.isRequired, // headline is a required string
    link: PropTypes.string.isRequired, // link is a required string
  }).isRequired, // data prop itself is required
}

export default Headline

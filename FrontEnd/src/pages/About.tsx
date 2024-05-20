import { motion } from 'framer-motion';
import { slideFromLeftAnimationVariants, textAnimationVariants } from '../static/variants';
import capstoneWhite from '/capstoneWhite.svg';
import { Link } from '@nextui-org/react';
import { BiSolidErrorAlt } from 'react-icons/bi';
import { FaBullseye } from 'react-icons/fa6';
import { FaMousePointer, FaBookOpen } from 'react-icons/fa';

export default function About() {
    return (
        <article className="h-full w-full">
            <section className="bg-family h-screen w-full bg-center bg-cover relative">
                <div className="h-full w-full bg-gradient-to-r from-10% from-white via-70% via-transparent"></div>
                <motion.div
                    className="text-[calc(4vw+1em)] font-semibold absolute top-[25%] max-md:text-center max-md:w-full px-12 text-pacific-blue leading-tight cursor-default"
                    initial="initial"
                    whileInView="animate"
                    viewport={{ once: true }}
                    exit="exit"
                    transition={{ ease: 'easeOut', duration: 0.5 }}
                    variants={slideFromLeftAnimationVariants}>
                    Enhance you provider data.
                    <br />
                    Enhance your peace of mind.
                    <br />
                    <div className="text-[#262626] leading-tight text-[0.5em]">Check your directory today</div>
                    <button
                        className="text-white bg-pacific-blue text-[0.3em] font-normal max-md:text-[0.4em] px-8 py-4 max-md:py-3 mt-5 rounded-md max-ms:w-full shadow-xl max-ms:drop-shadow-lg z-40 transition ease-in-out hover:scale-105"
                        onClick={() => (window.location.href = '/')}>
                        Get Started
                    </button>
                </motion.div>
            </section>
            <section className="bg-pacific-green h-full w-full justify-center items-center">
                <motion.header
                    className="flex self-center justify-center items-stretch bg-pacific-light-gray py-4 text-pacific-blue font-semibold text-[calc(2vw+1.5em)] text-center px-2"
                    initial="initial"
                    whileInView="animate"
                    viewport={{ once: true }}
                    exit="exit"
                    variants={textAnimationVariants}
                    transition={{ ease: 'easeOut', duration: 0.5, delay: 0.2 }}>
                    What are these APIs for?
                </motion.header>
                <motion.article
                    initial="initial"
                    whileInView="animate"
                    viewport={{ once: true }}
                    exit="exit"
                    variants={textAnimationVariants}
                    transition={{ ease: 'easeOut', duration: 0.5, delay: 0.2 }}
                    className="font-normal text-xl max-md:text-base text-center md:text-left text-pacific-light-gray md:grid md:grid-cols-2 md:gap-5 flex flex-col p-8">
                    <div className="py-5 self-center w-full">
                        <div className="font-bold text-3xl">The FHIRType API supports</div>
                        <div className="font-bold text-3xl mb-5">
                            any medical organization&rsquo;s provider directory.
                        </div>
                        <div>From insurance payers to referral offices,</div>
                        <div>FHIRType helps improve your provider directory</div>
                        <div>by aggregating data from major insurance payers&rsquo; public provider directories</div>
                        <div>and intelligently identifying potentially outdated information.</div>
                    </div>
                    <div className="h-[50vh] min-h-[400px] w-full bg-team bg-center bg-cover rounded-2xl"></div>
                </motion.article>
            </section>
            <section className="bg-pacific-blue from-10% bg-gradient-to-t from-[#19182f42] h-full w-full bg-center bg-cover relative py-12 justify-center items-center">
                <motion.header
                    className="flex self-center justify-center items-stretch text-pacific-light-gray font-semibold text-[calc(2vw+1.5em)] mb-6 text-center px-2"
                    initial="initial"
                    whileInView="animate"
                    viewport={{ once: true }}
                    exit="exit"
                    variants={textAnimationVariants}
                    transition={{ ease: 'easeOut', duration: 0.5, delay: 0.2 }}>
                    How can we serve better provider information?
                </motion.header>
                <div className="flex flex-col gap-6 w-full h-full justify-center items-center text-pacific-light-gray cursor-default self-center">
                    <motion.div
                        className="rounded border-2 border-pacific-light-blue px-4 py-6 w-[80%] md:w-[60%] text-center transition ease-in-out hover:bg-pacific-light-gray hover:text-pacific-blue hover:border-pacific-light-gray"
                        initial="initial"
                        whileInView="animate"
                        exit="exit"
                        viewport={{ once: true }}
                        transition={{ ease: 'easeOut', duration: 0.2 }}
                        variants={slideFromLeftAnimationVariants}>
                        <div className="font-medium text-xl">Interoperability</div>
                        <div className="font-normal text-base max-md:text-sm">
                            The Fast Healthcare Interoperability Resources framework provides a platform for building
                            interoperable data sharing.
                        </div>
                    </motion.div>
                    <motion.div
                        className="rounded border-2 border-pacific-light-blue px-4 py-6 w-[80%] md:w-[60%] text-center transition ease-in-out hover:bg-pacific-light-gray hover:text-pacific-blue hover:border-pacific-light-gray"
                        initial="initial"
                        whileInView="animate"
                        exit="exit"
                        viewport={{ once: true }}
                        transition={{ ease: 'easeOut', duration: 0.2 }}
                        variants={slideFromLeftAnimationVariants}>
                        <div className="font-medium text-xl">Integrity</div>
                        <div className="font-normal text-base max-md:text-sm">
                            Leveraging the wisdom of the crowd by comparing data from different sources combined with
                            modern GenAI techniques can improve error detection significantly.{' '}
                        </div>
                    </motion.div>
                    <motion.div
                        className="rounded border-2 border-pacific-light-blue px-4 py-6 w-[80%] mb-6 md:w-[60%] text-center transition ease-in-out hover:bg-pacific-light-gray hover:text-pacific-blue hover:border-pacific-light-gray"
                        initial="initial"
                        whileInView="animate"
                        exit="exit"
                        viewport={{ once: true }}
                        transition={{ ease: 'easeOut', duration: 0.2 }}
                        variants={slideFromLeftAnimationVariants}>
                        <div className="font-medium text-xl">Availability</div>
                        <div className="font-normal text-base max-md:text-sm">
                            Using modern continuous integration and deployment strategies combine with a quick API
                            framework, you can expect to get the data you need, when you need it.{' '}
                        </div>
                    </motion.div>
                </div>
            </section>

            <section className="bg-pacific-light-gray h-full w-full bg-center bg-cover relative py-12 justify-center items-center">
                <motion.header
                    className="flex self-center justify-center items-stretch text-pacific-blue font-semibold text-[calc(2vw+2em)] mb-12 text-center leading-10 px-2"
                    initial="initial"
                    whileInView="animate"
                    viewport={{ once: true }}
                    exit="exit"
                    variants={textAnimationVariants}
                    transition={{ ease: 'easeOut', duration: 0.5, delay: 0.2 }}>
                    How we can help
                </motion.header>
                <motion.div
                    className="flex h-full flex-wrap flex-row justify-center"
                    initial="initial"
                    whileInView="animate"
                    viewport={{ once: true }}
                    exit="exit"
                    variants={textAnimationVariants}
                    transition={{ ease: 'easeOut', duration: 0.5, delay: 0.5 }}>
                    <div className="from-transparent to-transparent text-pacific-blue flex md:flex-half md:h-[40vh] md:border-r md:border-b md:max-h-[400px] w-full h-[33vh] max-md:border-b border-pacific-blue items-center justify-center text-center transition ease-in-out hover:bg-pacific-blue  hover:text-pacific-light-gray">
                        <div className="flex flex-col px-2">
                            <div className="text-6xl text-center self-center">
                                <FaBullseye />
                            </div>
                            <div className="text-4xl font-semibold">Accuracy</div>
                            <div>Contributes to increase in provider data accuracy</div>
                            <div>Validate thousands of records faster</div>
                        </div>
                    </div>
                    <div className="from-transparent to-transparent text-pacific-blue flex md:flex-half md:h-[40vh] md:border-l md:border-b md:max-h-[400px] w-full h-[33vh] max-md:border-b border-pacific-blue items-center justify-center text-center transition ease-in-out hover:bg-pacific-blue  hover:text-pacific-light-gray">
                        <div className="flex flex-col px-2">
                            <div className="text-6xl text-center self-center">
                                <BiSolidErrorAlt />
                            </div>
                            <div className="text-4xl font-semibold">Error Detection</div>

                            <div>Accurately detect errors in data</div>
                            <div>Find records that need testifying</div>
                        </div>
                    </div>
                    <div className="from-transparent to-transparent text-pacific-blue flex md:flex-half md:h-[40vh] md:border-r md:border-t md:max-h-[400px] w-full h-[33vh] max-md:border-b border-pacific-blue items-center justify-center text-center transition ease-in-out hover:bg-pacific-blue  hover:text-pacific-light-gray">
                        <div className="flex flex-col px-2">
                            <div className="text-6xl text-center self-center">
                                <FaMousePointer />
                            </div>
                            <div className="text-4xl font-semibold">Ease of Use</div>
                            <div>Attractive and usable client right in your browser</div>
                            <div>Check provider data by hand or upload spreadsheets</div>
                        </div>
                    </div>
                    <div className="from-transparent to-transparent text-pacific-blue flex md:flex-half md:h-[40vh] md:border-l md:border-t md:max-h-[400px] w-full h-[33vh] border-pacific-blue items-center justify-center text-center transition ease-in-out hover:bg-pacific-blue  hover:text-pacific-light-gray">
                        <div className="flex flex-col px-2">
                            <div className="text-6xl text-center self-center">
                                <FaBookOpen />
                            </div>
                            <div className="text-4xl font-semibold">Open Source/Data</div>
                            <div>Documented and ready for open source contribution</div>
                            <div>Utilizes open data to improve accuracy</div>
                        </div>
                    </div>
                </motion.div>
            </section>
            <hr />
            <section className="bg-pacific-light-gray h-full w-full relative py-12 px-12 justify-center items-center">
                <header className="text-4xl font-semibold mb-3">FAQ</header>
                <div className="flex flex-col gap-4 text-lg">
                    <div>
                        <div className="font-semibold text-pacific-blue">
                            Q: Does this service adhere to HIPAA rules?
                        </div>
                        <div className="text-[#262626] leading-tight max-md:text-sm">
                            FHIRType doesn&rsquo;t handle any PHI, so it is not affected by HIPAA rules. Additionally,
                            FHIRType only connects to publicly available APIs out of the box, and since it&rsquo;s
                            open-source you can see the exact URIs that are used!
                        </div>
                    </div>
                    <div>
                        <div className="font-semibold text-pacific-blue">
                            Q: Can I connect to additional data sources?
                        </div>
                        <div className="text-[#262626] leading-tight max-md:text-sm">
                            FHIRType connects to FHIR-standard RESTful APIs out of the box. For an example of how this
                            works, see this section of the public repository.
                        </div>
                    </div>
                </div>
            </section>
            <footer className="grid justify-center grid-cols-2 md:grid-cols-4 gap-x-6 bg-[#262626] px-[20%] min-h-[10vh] h-full max-h-[250px] py-4 md:py-8 text-pacific-gray text-xs md:text-sm cursor-default">
                <div className="flex flex-col text-center gap-1 col-span-2 self-center">
                    <img
                        src={capstoneWhite}
                        alt="pacific source"
                        className={'w-[calc(12vw+10em)] self-center hover:cursor-pointer select-none max-md:pb-4'}
                        onClick={() => (window.location.href = '/')}
                    />
                </div>
                <div className="flex flex-col text-left gap-1">
                    <div className="font-bold md:text-base mb-2">Oregon State University</div>
                    <Link
                        className={'text-white text-sm max-md:text-xs'}
                        target={'_blank'}
                        underline={'always'}
                        href={'https://github.com/trentonyo'}>
                        Trenton Young
                    </Link>
                    <Link
                        className={'text-white text-sm max-md:text-xs'}
                        target={'_blank'}
                        underline={'always'}
                        href={'https://github.com/HlaKarki'}>
                        Hla Htun
                    </Link>
                    <Link
                        className={'text-white text-sm max-md:text-xs'}
                        target={'_blank'}
                        underline={'always'}
                        href={'https://github.com/ImgyeongLee'}>
                        Imgyeong Lee
                    </Link>
                    <Link
                        className={'text-white text-sm max-md:text-xs'}
                        target={'_blank'}
                        underline={'always'}
                        href={'https://github.com/IainRichey'}>
                        Iain Richey
                    </Link>
                    <Link
                        className={'text-white text-sm max-md:text-xs'}
                        target={'_blank'}
                        underline={'always'}
                        href={'https://github.com/valdovjo'}>
                        Jose Dani Valdovinos
                    </Link>
                </div>
                <div className="flex flex-col text-left gap-1">
                    <div className="font-bold md:text-base mb-2">PacificSource</div>
                    <div>Martin Martinez</div>
                    <div>Andrew Diestel</div>
                    <div>Kevin Carman</div>
                </div>
            </footer>
        </article>
    );
}
